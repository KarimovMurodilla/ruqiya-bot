"""User model file."""
import datetime
from typing import Annotated, Optional
import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Cart(Base):
    """Cart model."""

    user_id: Mapped[int] = mapped_column(sa.ForeignKey("user.user_id", ondelete="CASCADE"))
    product_id: Mapped[int] = mapped_column(sa.ForeignKey("product.id", ondelete="CASCADE"))
    total_count: Mapped[int] = mapped_column(
        sa.Integer, unique=False, nullable=True
    )
    total_price: Mapped[int] = mapped_column(
        sa.Numeric, unique=False, nullable=True
    )
    status: Mapped[bool] = mapped_column(
        sa.Boolean, default=True
    )
    created_at: Mapped[Optional[Annotated[datetime.datetime, mapped_column(nullable=False, default=datetime.datetime.utcnow)]]]

    def __str__(self):
        return f"{self.total_price}"
