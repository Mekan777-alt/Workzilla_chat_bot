from aiogram.types import ReplyKeyboardMarkup


def sos():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("✉ Написать сообщение", "📞 Позвонить")
    markup.add('👈 Назад')
    return markup
