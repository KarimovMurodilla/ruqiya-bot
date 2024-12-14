"""User model file."""
import datetime
import sqlalchemy as sa
import sqlalchemy.orm as orm

from typing import Annotated, Optional
from sqlalchemy.orm import Mapped, mapped_column

from src.bot.structures.role import Role

from .base import Base
from ...language.enums import Locales


class Product(Base):
    """Product model."""

    product_name: Mapped[str] = mapped_column(
        sa.Text, unique=False, nullable=True
    )
    price: Mapped[int] = mapped_column(
        sa.Numeric, unique=False, nullable=True
    )
    max_count: Mapped[int] = mapped_column(
        sa.Integer, unique=False, nullable=True
    )    
    min_count: Mapped[int] = mapped_column(
        sa.Integer, unique=False, nullable=True
    )
    created_at: Mapped[Optional[Annotated[datetime.datetime, mapped_column(nullable=False, default=datetime.datetime.utcnow)]]]

    def __str__(self):
        return f"{self.product_name}"
