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

    async def get_product(self, **filters):
        product = await self.session.scalar(
            select(Product).filter_by(**filters).limit(1)
        )

        return product
    
    async def get_all_products(self):
        result = await self.session.scalars(
            select(Product)
        )

        products = result.all()
        return products
    
    async def delete(self, product_id: int):
        await super().delete(Product.id == product_id)
        await self.session.commit()
