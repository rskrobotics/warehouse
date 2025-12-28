from uuid import UUID
from pydantic import BaseModel, EmailStr
from warehouse.models.store_settings import Currency


class SettingResponse(BaseModel):
    currency: Currency

    model_config = {"from_attributes": True}


class SkuResponse(BaseModel):
    uuid: UUID
    sku: str
    name: str

    model_config = {"from_attributes": True}


class ItemResponse(BaseModel):
    uuid: UUID
    quantity: int
    sku: SkuResponse

    model_config = {"from_attributes": True}


class ItemUpdateRequest(BaseModel):
    quantity: int


class StoreDetailResponse(BaseModel):
    uuid: UUID
    name: str
    code: str
    email: EmailStr
    is_active: bool
    settings: SettingResponse | None
    items: list[ItemResponse]

    model_config = {"from_attributes": True}
