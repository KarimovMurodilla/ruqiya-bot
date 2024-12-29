"""User model file."""
import datetime
from typing import Annotated, Optional, List
import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.bot.structures.role import Role

from .base import Base
from ...language.enums import Locales


class Order(Base):
    """Order model."""

    user_id: Mapped[int] = mapped_column(sa.ForeignKey("user.user_id", ondelete="CASCADE"))
    created_at: Mapped[Optional[Annotated[datetime.datetime, mapped_column(nullable=False, default=datetime.datetime.utcnow)]]]
    order_items: Mapped[List["OrderItem"]] = relationship("OrderItem", back_populates="order", lazy="joined")
    approved_orders = relationship("ApprovedOrder", back_populates="order")

    def __str__(self):
        return f"{self.user_id}"


class OrderItem(Base):
    """OrderItem model."""

    user_id: Mapped[int] = mapped_column(
        sa.ForeignKey("user.user_id", ondelete="CASCADE")
    )
    order_id: Mapped[int] = mapped_column(
        sa.ForeignKey("order.id", ondelete="CASCADE")
    )
    product_name: Mapped[str] = mapped_column(
        sa.String(100), unique=False, nullable=True
    )
    total_price: Mapped[int] = mapped_column(
        sa.Numeric, unique=False, nullable=True
    )
    total_count: Mapped[int] = mapped_column(
        sa.Integer, unique=False, nullable=True
    )
    status: Mapped[bool] = mapped_column(
        sa.Boolean, default=True
    )
    lat_long: Mapped[str] = mapped_column(
        sa.String(100), unique=False, nullable=True
    )
    created_at: Mapped[Optional[Annotated[datetime.datetime, mapped_column(nullable=False, default=datetime.datetime.utcnow)]]]

    order: Mapped[Order] = relationship("Order", back_populates="order_items")

    def __str__(self):
        return f"{self.total_price}"

