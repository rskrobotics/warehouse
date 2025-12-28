from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from warehouse.models.base import AuditMixin, Base


class Item(Base, AuditMixin):
    __tablename__ = "items"
    id: Mapped[int] = mapped_column(primary_key=True)
    store_id: Mapped[int] = mapped_column(ForeignKey("stores.id"))
    sku_id: Mapped[int] = mapped_column(ForeignKey("skus.id"))
    quantity: Mapped[int]

    store: Mapped["Store"] = relationship(back_populates="items")
    sku: Mapped["SKU"] = relationship(back_populates="items")
