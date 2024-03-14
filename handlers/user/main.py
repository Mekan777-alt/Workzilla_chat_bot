from aiogram import types
from aiogram import Router
from aiogram.filters import Command
from buttons.user.main import main_markup

router = Router()


@router.message(Command('start'))
async def start(message: types.Message):
    await message.answer(f"Дабро пожаловать {message.from_user.first_name} {message.from_user.last_name}",
                         reply_markup=main_markup())
