from sqlalchemy.orm import Mapped, mapped_column, relationship
from warehouse.models.base import Base, AuditMixin


class Supplier(Base, AuditMixin):
    __tablename__ = "suppliers"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str | None]
    code: Mapped[str] = mapped_column(unique=True)

    skus: Mapped[list["SKU"]] = relationship(
        secondary="supplier_skus", back_populates="suppliers"
    )
