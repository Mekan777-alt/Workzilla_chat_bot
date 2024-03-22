from aiogram.types import ReplyKeyboardMarkup


def loyal_markup_admin():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("Просмотреть пользователей")
    markup.add("Обновить баланс")
    return markup


def back_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("На главное")
    return markup

