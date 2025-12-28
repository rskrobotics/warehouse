from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from warehouse.repositories.store_repository import StoreRepository
from warehouse.schemas.schemas import StoreDetailResponse


class StoreService:
    def __init__(self, session: AsyncSession):
        self.repository = StoreRepository(session)

    async def get_by_uuid(self, uuid: UUID) -> StoreDetailResponse | None:
        store = await self.repository.get_by_uuid(uuid)
        if not store:
            return None
        return StoreDetailResponse.model_validate(store)

    async def get_by_code(self, code: str) -> StoreDetailResponse | None:
        store = await self.repository.get_by_code(code)
        if not store:
            return None
        return StoreDetailResponse.model_validate(store)
