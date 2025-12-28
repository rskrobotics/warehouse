from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from warehouse.db.database import get_db
from warehouse.schemas.schemas import ItemResponse, ItemUpdateRequest
from warehouse.services.item_service import ItemService

router = APIRouter(prefix="/items", tags=["items"])


@router.patch("/{uuid}", response_model=ItemResponse)
async def update_item_quantity(
    uuid: UUID,
    payload: ItemUpdateRequest,
    session: AsyncSession = Depends(get_db),
):
    """Update item quantity."""
    service = ItemService(session)
    item = await service.update_quantity(uuid, payload.quantity)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item
