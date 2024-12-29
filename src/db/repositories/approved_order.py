"""ApprovedOrder repository file."""

from sqlalchemy import select, update
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from src.bot.structures.role import Role

from ..models import Base, ApprovedOrder
from .abstract import Repository


class ApprovedOrderRepo(Repository[ApprovedOrder]):
    """ApprovedOrder repository for CRUD and other SQL queries."""

    def __init__(self, session: AsyncSession):
        """Initialize ApprovedOrder repository as for all ApprovedOrders or only for one ApprovedOrder."""
        super().__init__(type_model=ApprovedOrder, session=session)

    async def new(
        self,
        user_id: int, 
        order_id: int,
    ) -> None:
        await self.session.merge(
            ApprovedOrder(
                user_id=user_id,
                order_id=order_id
            )
        )
        await self.session.commit()

    async def get_approved_order_with_joined_data(self):
        query = (
            select(ApprovedOrder)
            # .join(ApprovedOrder.user) # INNER JOIN
            .join(ApprovedOrder.order) # INNER JOIN
            .where(ApprovedOrder.status == False)
            .options(joinedload(ApprovedOrder.user))  # Eager load items
            .options(joinedload(ApprovedOrder.order))  # Eager load items
        )
        result = await self.session.execute(query)
        return result.scalars().unique().all()

    async def set_status_checked(self) -> None:
        stmt = update(ApprovedOrder).values(status=True)
        await self.session.execute(stmt)
        await self.session.commit()

