"""Database class with all-in-one features."""

from sqlalchemy.engine.url import URL
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine as _create_async_engine

from src.configuration import conf

from .repositories import (
    UserRepo, ProductRepo, OrderRepo, CartRepo, ApprovedOrderRepo
)


def create_async_engine(url: URL | str) -> AsyncEngine:
    """Create async engine with given URL.

    :param url: URL to connect
    :return: AsyncEngine
    """
    return _create_async_engine(url=url, echo=conf.debug, pool_pre_ping=True)


class Database:
    """Database class.

    is the highest abstraction level of database and
    can be used in the handlers or any others bot-side functions.
    """

    user: UserRepo
    product: ProductRepo
    order: OrderRepo
    cart: CartRepo
    approved_order: ApprovedOrderRepo

    session: AsyncSession

    def __init__(
        self,
        session: AsyncSession,
        user: UserRepo = None,
        product: ProductRepo = None,
        order: OrderRepo = None,
        cart: CartRepo = None,
        approved_order: ApprovedOrderRepo = None,
    ):
        """Initialize Database class.

        :param session: AsyncSession to use
        """
        self.session = session
        self.user = user or UserRepo(session=session)
        self.product = product or ProductRepo(session=session)
        self.order = order or OrderRepo(session=session)
        self.cart = cart or CartRepo(session=session)
        self.approved_order = approved_order or ApprovedOrderRepo(session=session)
