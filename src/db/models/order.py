import datetime
import sqlalchemy as sa

from enum import Enum
from typing import Annotated, Optional, List
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class OrderStatus(Enum):
    PENDING = "pending"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class Order(Base):
    """Order model."""

    user_id: Mapped[int] = mapped_column(sa.ForeignKey("user.user_id", ondelete="CASCADE"))
    status: Mapped[OrderStatus] = mapped_column(sa.Enum(OrderStatus), nullable=True, default=OrderStatus.PENDING)
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

