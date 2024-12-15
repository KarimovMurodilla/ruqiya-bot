"""User repository file."""

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.bot.structures.role import Role

from ..models import Base, Cart
from .abstract import Repository


class CartRepo(Repository[Cart]):
    """Cart repository for CRUD and other SQL queries."""

    def __init__(self, session: AsyncSession):
        super().__init__(type_model=Cart, session=session)

    async def new(
        self,
        user_id: int,
        product_id: int,
        total_price: int,
        total_count: int,
    ) -> None:
        await self.session.merge(
            Cart(
                user_id=user_id,
                product_id=product_id,
                total_price=total_price,
                total_count=total_count,
            )
        )
        await self.session.commit()

    async def get(self, id: int) -> Cart:
        return await self.session.scalar(
            select(Cart).where(Cart.id == id).limit(1)
        )
    
    async def get_cart_products(self, user_id: int):
        result = await self.session.scalars(
            select(Cart).where(Cart.user_id == user_id and Cart.status == True)
        )

        cart_products = result.all()
        return cart_products

    async def update_cart(self, user_id: int, cart_id: int, **kwargs):
        # async with self.session.begin():
        stmt = (
            update(Cart)
            .where(Cart.user_id == user_id and Cart.id == cart_id)
            .values(**kwargs)
        )
        await self.session.execute(stmt)
        await self.session.commit()

    async def delete_cart(self, cart_id: int) -> None:
        await super().delete(Cart.id == cart_id)

