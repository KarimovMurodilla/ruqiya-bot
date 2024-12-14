"""User repository file."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.bot.structures.role import Role

from ..models import Base, Product
from .abstract import Repository


class ProductRepo(Repository[Product]):
    """Product repository for CRUD and other SQL queries."""

    def __init__(self, session: AsyncSession):
        super().__init__(type_model=Product, session=session)

    async def new(
        self,
        product_name: int,
        price: str | None = None,
        min_count: str | None = None,
    ) -> None:
        await self.session.merge(
            Product(
                product_name=product_name,
                price=price,
                min_count=min_count,
            )
        )
        await self.session.commit()

    async def get_all_products(self):
        result = await self.session.scalars(
            select(Product)
        )

        products = result.all()
        return products
