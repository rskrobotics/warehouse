from sqlalchemy.orm import Mapped, mapped_column
from warehouse.models.base import AuditMixin, Base


class SKU(Base, AuditMixin):
    __tablename__ = "skus"
    id: Mapped[int] = mapped_column(primary_key=True)
    sku: Mapped[str] = mapped_column(unique=True)
    ean: Mapped[str | None] = mapped_column(unique=True)
    name: Mapped[str]
    description: Mapped[str | None]
