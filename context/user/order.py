from aiogram.fsm.state import State, StatesGroup


class UserOrder(StatesGroup):
    user_name = State()
    brand_auto = State()
    color_auto = State()
    number_auto = State()

