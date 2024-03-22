from aiogram.types import ReplyKeyboardMarkup


def main():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('📖 Меню')
    markup.add('🕗 Режим работы', '? Помощь')
    markup.add('🎒 Заказать')
    return markup

