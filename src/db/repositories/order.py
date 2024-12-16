"""User repository file."""

from datetime import datetime, timedelta

from sqlalchemy import select, and_
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

    async def get_all_by_user_id(self, user_id: int):
        result = await self.session.scalars(
            select(Order).where(Order.user_id == user_id)
        )
        orders = result.all()
        return orders
        
    async def get_order(self, **filters):
        product = await self.session.scalar(
            select(Order).filter_by(**filters).limit(1)
        )
        return product

    async def get_orders(self, filters):
        result = await self.session.execute(
            select(Order).where(filters)
        )
        return result.scalars().all()

    async def get_orders_by_day(self, date):
        start = datetime.combine(date, datetime.min.time())
        end = datetime.combine(date, datetime.max.time())
        filters = and_(Order.created_at >= start, Order.created_at <= end)
        return await self.get_orders(filters)

    async def get_orders_by_week(self, start_date):
        start = datetime.combine(start_date, datetime.min.time())
        end = start + timedelta(days=6, hours=23, minutes=59, seconds=59)
        filters = and_(Order.created_at >= start, Order.created_at <= end)
        return await self.get_orders(filters)

    async def get_orders_by_month(self, year, month):
        start = datetime(year, month, 1)
        if month == 12:
            end = datetime(year + 1, 1, 1) - timedelta(seconds=1)
        else:
            end = datetime(year, month + 1, 1) - timedelta(seconds=1)
        filters = and_(Order.created_at >= start, Order.created_at <= end)
        return await self.get_orders(filters)
