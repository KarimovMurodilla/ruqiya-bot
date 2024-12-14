from aiogram.fsm.state import StatesGroup, State


class OrderGroup(StatesGroup): 
    get_product = State()
    to_order = State()
    get_count = State()
    show_regions = State()
    show_districts = State()
    get_geo = State()
