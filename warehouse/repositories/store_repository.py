from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from warehouse.models import Store, Item


class StoreRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    def _eager_load_options(self):
        """Common eager loading options for Store queries."""
        return [
            selectinload(Store.settings),
            selectinload(Store.items).selectinload(Item.sku),
        ]

    async def get_by_uuid(self, uuid: UUID) -> Store | None:
        stmt = (
            select(Store)
            .where(Store.uuid == uuid)
            .options(*self._eager_load_options())
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_code(self, code: str) -> Store | None:
        stmt = (
            select(Store)
            .where(Store.code == code)
            .options(*self._eager_load_options())
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def add_item(self, store: Store, item: Item) -> None:
        store.items.append(item)
        await self.session.flush()

