from config import dp, bot
from aiogram import types


@dp.message_handler(text='🕗 Режим работы')
async def time_work(message: types.Message):

    await message.answer("Режим работы если есть")
    # await message.answer("Happy People\n"
    #                      "Cafe Food & Drink\n"
    #                      "\n"
    #                      "Режим работы:\n"
    #                      "ВС-ЧТ\n"
    #                      "С 11:00 до 00:00\n"
    #                      "ПТ-СБ\n"
    #                      "C 11:00 до 02:00\n"
    #                      "\n"
    #                      "Адрес: Мусина 1\n"
    #                      "\n"
    #                      "☎️ Тел:  +7 (843) 225-06-06\n")
    # await bot.send_location(message.from_user.id, latitude=55.81693801144643, longitude=49.11948637935675)
