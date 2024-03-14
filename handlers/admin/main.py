from aiogram import Router, types
from aiogram.filters import Command

from buttons.admin.main import main_markup

router = Router()


@router.message(Command('admin'))
async def start(message: types.Message):
    await message.answer(f"Дабро пожаловать {message.from_user.first_name} {message.from_user.last_name}",
                         reply_markup=main_markup())
