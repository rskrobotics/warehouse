from sqlalchemy.orm import Mapped, mapped_column, relationship
from warehouse.models.base import AuditMixin, Base


class SKU(Base, AuditMixin):
    __tablename__ = "skus"
    id: Mapped[int] = mapped_column(primary_key=True)
    sku: Mapped[str] = mapped_column(unique=True)
    ean: Mapped[str | None] = mapped_column(unique=True)
    name: Mapped[str]
    description: Mapped[str | None]

    items: Mapped[list["Item"]] = relationship(back_populates="sku")
    suppliers: Mapped[list["Supplier"]] = relationship(
        secondary="supplier_skus", back_populates="skus"
    )
