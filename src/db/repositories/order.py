"""User repository file."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.bot.structures.role import Role

from ..models import Base, Order
from .abstract import Repository


class OrderRepo(Repository[Order]):
    """Order repository for CRUD and other SQL queries."""

    def __init__(self, session: AsyncSession):
        super().__init__(type_model=Order, session=session)

    async def new(
        self,
        user_id: int,
        total_price: int,
        lat_long: str
    ) -> None:
        await self.session.merge(
            Order(
                user_id=user_id,
                total_price=total_price,
                lat_long=lat_long
            )
        )
        await self.session.commit()

    async def get(self, id: int) -> Order:
        return await self.session.scalar(
            select(Order).where(Order.id == id).limit(1)
        )

    async def get_all_by_user_id(self, user_id: int):
        result = await self.session.scalars(
            select(Order).where(Order.user_id == user_id)
        )
        orders = result.all()
        return orders
        
