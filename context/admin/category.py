from aiogram.fsm.state import State, StatesGroup


class CategoryState(StatesGroup):
    name = State()

