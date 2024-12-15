from aiogram.fsm.state import StatesGroup, State


class AdminGroup(StatesGroup):
    broadcast = State()

    add_product = State()
    add_price = State()

    delete_product = State()

    set_min_sum = State()

