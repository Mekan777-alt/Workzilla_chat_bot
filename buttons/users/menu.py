from aiogram.types import ReplyKeyboardMarkup


def menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('🍣 Авторские роллы от Шефа Суши')
    markup.add('🥘 Основное меню')
    markup.add('🥗 Холодные закуски')
    markup.add('🍕 Выпечка/Пицца')
    markup.add('👈 Назад')
    return markup


def bar_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🍸 Алкогольные напитки")
    markup.add("☕ Безалкогольные напитки")
    markup.add('👈 Назад')
    return markup
