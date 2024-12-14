from aiogram.fsm.state import StatesGroup, State


class RegisterGroup(StatesGroup):
    """Use this state for registration"""
    
    lang = State()
    fullname = State()
    phone_number = State()

    # Settings
    choose_option = State()
    change_lang = State()
    change_phone_number = State()
    change_fullname = State()
