"""seed test data

Revision ID: bcf7ddcbd8b3
Revises: ef54818b8f80
Create Date: 2025-12-28 19:37:36.064625

"""
from typing import Sequence, Union
from uuid import uuid4

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bcf7ddcbd8b3'
down_revision: Union[str, Sequence[str], None] = '815d78acc0b2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    conn = op.get_bind()

    # Insert stores
    conn.execute(sa.text("""
        INSERT INTO stores (name, code, email, address, is_active, uuid, version, created_at, updated_at)
        VALUES
            ('Main Warehouse', 'WH-001', 'main@warehouse.com', '123 Storage Lane', true, :uuid1, 1, NOW(), NOW()),
            ('Secondary Depot', 'WH-002', 'depot@warehouse.com', '456 Depot Road', true, :uuid2, 1, NOW(), NOW()),
            ('Outlet Store', 'WH-003', 'outlet@warehouse.com', NULL, false, :uuid3, 1, NOW(), NOW())
    """), {"uuid1": str(uuid4()), "uuid2": str(uuid4()), "uuid3": str(uuid4())})

    # Insert store settings
    conn.execute(sa.text("""
        INSERT INTO store_settings (store_id, currency, uuid, version, created_at, updated_at)
        SELECT id, 'EUR', :uuid1, 1, NOW(), NOW() FROM stores WHERE code = 'WH-001'
    """), {"uuid1": str(uuid4())})

    conn.execute(sa.text("""
        INSERT INTO store_settings (store_id, currency, uuid, version, created_at, updated_at)
        SELECT id, 'PLN', :uuid1, 1, NOW(), NOW() FROM stores WHERE code = 'WH-002'
    """), {"uuid1": str(uuid4())})

    # Insert items (inventory) - link stores to SKUs
    conn.execute(sa.text("""
        INSERT INTO items (store_id, sku_id, quantity, uuid, version, created_at, updated_at)
        SELECT s.id, k.id, 100, :uuid, 1, NOW(), NOW()
        FROM stores s, skus k WHERE s.code = 'WH-001' AND k.sku = 'PAINT-WHT-1L'
    """), {"uuid": str(uuid4())})

    conn.execute(sa.text("""
        INSERT INTO items (store_id, sku_id, quantity, uuid, version, created_at, updated_at)
        SELECT s.id, k.id, 50, :uuid, 1, NOW(), NOW()
        FROM stores s, skus k WHERE s.code = 'WH-001' AND k.sku = 'PAINT-BLK-1L'
    """), {"uuid": str(uuid4())})

    conn.execute(sa.text("""
        INSERT INTO items (store_id, sku_id, quantity, uuid, version, created_at, updated_at)
        SELECT s.id, k.id, 25, :uuid, 1, NOW(), NOW()
        FROM stores s, skus k WHERE s.code = 'WH-001' AND k.sku = 'PRIMER-1L'
    """), {"uuid": str(uuid4())})

    conn.execute(sa.text("""
        INSERT INTO items (store_id, sku_id, quantity, uuid, version, created_at, updated_at)
        SELECT s.id, k.id, 200, :uuid, 1, NOW(), NOW()
        FROM stores s, skus k WHERE s.code = 'WH-002' AND k.sku = 'PAINT-WHT-5L'
    """), {"uuid": str(uuid4())})

    # Insert suppliers
    conn.execute(sa.text("""
        INSERT INTO suppliers (name, code, uuid, version, created_at, updated_at)
        VALUES
            ('Paint Co', 'SUP-001', :uuid1, 1, NOW(), NOW()),
            ('Primer Plus', 'SUP-002', :uuid2, 1, NOW(), NOW())
    """), {"uuid1": str(uuid4()), "uuid2": str(uuid4())})

    # Link suppliers to SKUs (many-to-many)
    conn.execute(sa.text("""
        INSERT INTO supplier_skus (supplier_id, sku_id)
        SELECT sup.id, sku.id FROM suppliers sup, skus sku
        WHERE sup.code = 'SUP-001' AND sku.sku IN ('PAINT-WHT-1L', 'PAINT-BLK-1L', 'PAINT-RED-1L')
    """))

    conn.execute(sa.text("""
        INSERT INTO supplier_skus (supplier_id, sku_id)
        SELECT sup.id, sku.id FROM suppliers sup, skus sku
        WHERE sup.code = 'SUP-002' AND sku.sku = 'PRIMER-1L'
    """))


def downgrade() -> None:
    """Downgrade schema."""
    conn = op.get_bind()
    conn.execute(sa.text("DELETE FROM supplier_skus"))
    conn.execute(sa.text("DELETE FROM suppliers"))
    conn.execute(sa.text("DELETE FROM items"))
    conn.execute(sa.text("DELETE FROM store_settings"))
    conn.execute(sa.text("DELETE FROM stores"))
