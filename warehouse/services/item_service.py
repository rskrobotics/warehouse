from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from warehouse.repositories.item_repository import ItemRepository
from warehouse.schemas.schemas import ItemResponse


class ItemService:
    def __init__(self, session: AsyncSession):
        self.repository = ItemRepository(session)

    async def update_quantity(self, uuid: UUID, quantity: int) -> ItemResponse | None:
        item = await self.repository.update_quantity(uuid, quantity)
        if not item:
            return None
        return ItemResponse.model_validate(item)
