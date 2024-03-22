import asyncio
import logging
from datetime import datetime
from buttons.users.main import main
from config import dp, db, loop, bot
import heandlers
import aioschedule
from aiogram import executor, types
from aiogram.dispatcher import FSMContext


@dp.message_handler(commands='start', state="*")
async def start(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer('ДОБРО ПОЖАЛОВАТЬ, {0.first_name}\n'
                         'Я Ваш личный бот, помощник.\n'
                         'Я помогу Вам ознакомиться с меню, режимом работы'.format(
        message.from_user), reply_markup=main())


async def on_startup(_):
    logging.basicConfig(level=logging.INFO)
    db.create_tables()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=False, on_startup=on_startup, loop=loop)
