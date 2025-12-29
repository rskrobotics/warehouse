from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from warehouse.models import Item


class ItemRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def update_quantity(self, uuid: UUID, quantity: int) -> Item | None:
        """
        Update item quantity by UUID.

        TODO: Implement this method:
        1. Fetch the item by uuid
        2. If not found, return None
        3. Update the quantity
        4. Flush the session
        5. Return the updated item

        Hint: You can use select() to fetch, then modify the object directly.
        SQLAlchemy tracks changes automatically.
        """
        stmt = select(Item).where(Item.uuid == uuid).options(selectinload(Item.sku))
        result = await self.session.execute(stmt)
        item = result.scalar_one_or_none()
        if not item:
            return None
        item.quantity = quantity
        await self.session.flush()
        return item
