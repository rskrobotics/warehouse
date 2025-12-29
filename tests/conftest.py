import pytest
from httpx import AsyncClient, ASGITransport
from testcontainers.postgres import PostgresContainer
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from warehouse.main import app
from warehouse.db.database import get_db
from warehouse.models import SKU, Store, Item


@pytest.fixture(scope="session")
def postgres_container():
    with PostgresContainer("postgres:16") as container:
        yield container


@pytest.fixture(scope="session")
def database_url(postgres_container):
    return postgres_container.get_connection_url().replace(
        "postgresql+psycopg2", "postgresql+asyncpg"
    )


@pytest.fixture(scope="function")
async def engine(database_url):
    """Create engine per test to avoid event loop issues."""
    engine = create_async_engine(database_url, echo=False)

    # Create tables
    from warehouse.models import Base
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    # Drop tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest.fixture(scope="function")
async def session(engine):
    """Fresh session per test, rollback after."""
    async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session
        await session.rollback()


@pytest.fixture(scope="function")
async def client(session):
    """HTTP client with test database injected."""

    async def override_get_db():
        yield session

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        yield client

    app.dependency_overrides.clear()


# =============================================================================
# Test Data Fixtures
# =============================================================================


@pytest.fixture
async def sample_sku(session):
    """Create a basic SKU."""
    sku = SKU(name="Test Widget", sku="TEST-001")
    session.add(sku)
    await session.flush()
    return sku


@pytest.fixture
async def sample_store(session):
    """Create a basic Store."""
    store = Store(name="Test Warehouse", code="WH-TEST", email="test@example.com")
    session.add(store)
    await session.flush()
    return store


@pytest.fixture
async def sample_item(session, sample_sku, sample_store):
    """Create an Item (depends on SKU and Store)."""
    item = Item(sku=sample_sku, store=sample_store, quantity=100)
    session.add(item)
    await session.flush()
    return item
