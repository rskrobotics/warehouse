from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from warehouse.db.database import get_db
from warehouse.schemas.schemas import StoreDetailResponse
from warehouse.services.store_service import StoreService

router = APIRouter(prefix="/stores", tags=["stores"])


@router.get("/{uuid}", response_model=StoreDetailResponse)
async def get_store(uuid: UUID, session: AsyncSession = Depends(get_db)):
    """Get store by UUID (primary access)."""
    service = StoreService(session)
    store = await service.get_by_uuid(uuid)
    if not store:
        raise HTTPException(status_code=404, detail="Store not found")
    return store


@router.get("/", response_model=StoreDetailResponse | None)
async def find_store(code: str, session: AsyncSession = Depends(get_db)):
    """Find store by code (search/lookup)."""
    service = StoreService(session)
    store = await service.get_by_code(code)
    if not store:
        raise HTTPException(status_code=404, detail="Store not found")
    return store
