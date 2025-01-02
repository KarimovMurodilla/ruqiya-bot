"""User repository file."""

from datetime import datetime, timedelta

from sqlalchemy import select, and_, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from .abstract import Repository
from ..models.order import Order, OrderItem, OrderStatus


class OrderRepo(Repository[Order]):
    """Order repository for CRUD and other SQL queries."""

    def __init__(self, session: AsyncSession):
        super().__init__(type_model=Order, session=session)

    async def new(
        self,
        user_id: int
    ) -> int:
        order_id = await self._create_order(user_id=user_id)
        return order_id

    async def new_item(
        self,
        order_id: int,
        user_id: int,
        product_name: str,
        total_price: int,
        total_count: int,
        lat_long: str
    ) -> None:
        await self._create_order_item(
            user_id=user_id,
            order_id=order_id,
            product_name=product_name,
            total_price=total_price,
            total_count=total_count,
            lat_long=lat_long
        )
    
    async def _create_order(
        self,
        user_id: int
    ) -> None:
        stmt = insert(Order).values(user_id=user_id).returning(Order.id)
        result = await self.session.execute(stmt)
        order_id = result.scalars().one()

        return order_id

    async def _create_order_item(
        self,
        user_id: int,
        order_id: int,
        product_name: str,
        total_price: int,
        total_count: int,
        lat_long: str
    ) -> None:
        await self.session.merge(
            OrderItem(
                user_id=user_id,
                order_id=order_id,
                product_name=product_name,
                total_price=total_price,
                total_count=total_count,
                lat_long=lat_long
            )
        )
        await self.session.commit()

    async def get_all_by_user_id(self, user_id: int):
        result = await self.session.scalars(
            select(OrderItem).where(OrderItem.user_id == user_id)
        )
        orders = result.all()
        return orders

    async def update_status(self, order_id: int, status: OrderStatus):
        stmt = (
            update(Order)
            .where(Order.id == order_id)
            .values(status=status)
        )
        await self.session.execute(stmt)
        await self.session.commit()

    async def filter_orders(self, **filters):
        result = await self.session.execute(
            select(Order).filter_by(**filters)
        )
        return result.unique().scalars().all()
    
    async def delete_order(self, order_id: int):
        stmt = delete(Order).where(Order.id == order_id)
        await self.session.execute(stmt)
        await self.session.commit()

    
    # OrderItem methods
    async def get_orders(self, filters):
        result = await self.session.execute(
            select(OrderItem).where(filters)
        )
        return result.scalars().all()

    async def get_orders_by_day(self, date):
        start = datetime.combine(date, datetime.min.time())
        end = datetime.combine(date, datetime.max.time())
        filters = and_(OrderItem.created_at >= start, OrderItem.created_at <= end)
        return await self.get_orders(filters)

    async def get_orders_by_week(self, start_date):
        start = datetime.combine(start_date, datetime.min.time())
        end = start + timedelta(days=6, hours=23, minutes=59, seconds=59)
        filters = and_(OrderItem.created_at >= start, OrderItem.created_at <= end)
        return await self.get_orders(filters)

    async def get_orders_by_month(self, year, month):
        start = datetime(year, month, 1)
        if month == 12:
            end = datetime(year + 1, 1, 1) - timedelta(seconds=1)
        else:
            end = datetime(year, month + 1, 1) - timedelta(seconds=1)
        filters = and_(OrderItem.created_at >= start, OrderItem.created_at <= end)
        return await self.get_orders(filters)
    
