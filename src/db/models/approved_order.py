"""User model file."""
import datetime
import sqlalchemy as sa

from typing import Annotated, Optional, List
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .user import User
from .order import Order


class ApprovedOrder(Base):
    """ApprovedOrder model."""

    user_id: Mapped[int] = mapped_column(sa.ForeignKey("user.user_id", ondelete="CASCADE"))
    order_id: Mapped[int] = mapped_column(sa.ForeignKey("order.id", ondelete="CASCADE"))
    status: Mapped[bool] = mapped_column(sa.Boolean, default=False)
    created_at: Mapped[Optional[Annotated[datetime.datetime, mapped_column(nullable=False, default=datetime.datetime.utcnow)]]]

    user: Mapped[User] = relationship("User", back_populates="approved_orders")
    order: Mapped[Order] = relationship("Order", back_populates="approved_orders")

    def __str__(self):
        return f"{self.user_id}"
