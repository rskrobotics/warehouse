from datetime import datetime
from uuid import uuid4, UUID
from sqlalchemy import func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class AuditMixin:
    uuid: Mapped[UUID] = mapped_column(default=uuid4, unique=True)
    version: Mapped[int] = mapped_column(default=1)
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        default=func.now(), onupdate=func.now()
    )
    deleted_at: Mapped[datetime | None] = mapped_column(default=None)

    __mapper_args__ = {"version_id_col": "version"}


# Define your models here by inheriting from Base
# Example:
#
# from sqlalchemy import String, Integer, ForeignKey
# from sqlalchemy.orm import Mapped, mapped_column, relationship
#
# class Product(Base):
#     __tablename__ = "products"
#
#     id: Mapped[int] = mapped_column(primary_key=True)
#     name: Mapped[str] = mapped_column(String(100))
#     sku: Mapped[str] = mapped_column(String(50), unique=True)
