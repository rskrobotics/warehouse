from sqlalchemy.orm import Mapped, mapped_column
from warehouse.models.base import AuditMixin, Base


class Store(Base, AuditMixin):
    __tablename__ = "stores"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    code: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str]
    address: Mapped[str | None]
    is_active: Mapped[bool] = mapped_column(default=True)
