from config import dp, bot
from aiogram import types


@dp.message_handler(text='🕗 Режим работы')
async def time_work(message: types.Message):

    await message.answer("Рабочее время каждого дня, за исключением понедельника, начинается в 11:00 и заканчивается в "
                         "19:00. Время на обед - с 15:00 до 16:00.")
