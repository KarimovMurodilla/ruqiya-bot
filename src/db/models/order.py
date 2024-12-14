"""User model file."""
import datetime
from typing import Annotated, Optional
import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Mapped, mapped_column

from src.bot.structures.role import Role

from .base import Base
from ...language.enums import Locales


class Order(Base):
    """Order model."""

    user_id: Mapped[int] = mapped_column(sa.ForeignKey("user.user_id", ondelete="CASCADE"))

    total_price: Mapped[int] = mapped_column(
        sa.Numeric, unique=False, nullable=True
    )
    status: Mapped[bool] = mapped_column(
        sa.Boolean, default=True
    )
    lat_long: Mapped[str] = mapped_column(
        sa.String(100), unique=False, nullable=True
    )
    created_at: Mapped[Optional[Annotated[datetime.datetime, mapped_column(nullable=False, default=datetime.datetime.utcnow)]]]

    def __str__(self):
        return f"{self.total_price}"
