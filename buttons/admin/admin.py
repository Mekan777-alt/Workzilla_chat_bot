from aiogram.types import ReplyKeyboardMarkup


def admin():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('⚙️ Настройка каталога', '⚙️ Настройка режима')
    markup.add("⚙ Старт/Стоп позиций")
    return markup

