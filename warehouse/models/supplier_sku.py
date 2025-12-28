from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from warehouse.models.base import Base


class SupplierSKU(Base):
    __tablename__ = "supplier_skus"
    supplier_id: Mapped[int] = mapped_column(
        ForeignKey("suppliers.id"), primary_key=True
    )
    sku_id: Mapped[int] = mapped_column(ForeignKey("skus.id"), primary_key=True)
