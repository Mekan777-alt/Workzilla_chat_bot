from config import dp, db
from aiogram import types
from buttons.admin.settings_catalog import catalog


@dp.message_handler(text='⚙️ Настройка каталога')
async def settings_catalog(message: types.Message):
    await message.answer('Выберите каталог', reply_markup=catalog())

