from enum import Enum
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from warehouse.models.base import AuditMixin, Base


class Currency(str, Enum):
    PLN = "PLN"
    YEN = "YEN"
    EUR = "EUR"


class StoreSettings(Base, AuditMixin):
    __tablename__ = "store_settings"
    id: Mapped[int] = mapped_column(primary_key=True)
    store_id: Mapped[int] = mapped_column(ForeignKey("stores.id"), unique=True)
    currency: Mapped[Currency]

    store: Mapped["Store"] = relationship(back_populates="settings")
