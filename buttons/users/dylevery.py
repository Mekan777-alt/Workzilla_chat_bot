from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from aiogram.utils.callback_data import CallbackData
from config import db

product_cb = CallbackData('product', 'id', 'action')


def product_markup(idx='', check=None):
    markup = InlineKeyboardMarkup()
    if check:
        markup.add(
            InlineKeyboardButton(f'Заказать за мешок', callback_data=product_cb.new(id=idx, action=f'add_{"meshok"}')))

        markup.add(InlineKeyboardButton('Заказать по кг', callback_data=product_cb.new(id=idx, action=f'add_{"kg"}')))
    else:
        markup.add(InlineKeyboardButton('Заказать', callback_data=product_cb.new(id=idx, action='add')))
    return markup


category_cb = CallbackData('category', 'id', 'action')


def categories_markup():
    markup = InlineKeyboardMarkup()
    for idx, title in db.fetchall('SELECT * FROM categories'):
        markup.add(InlineKeyboardButton(title, callback_data=category_cb.new(id=idx, action='view_2')))

    return markup


def menu_markup():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('📖 МЕНЮ', '🛒 Перейти в Корзину')
    markup.add('👈 Назад')
    return markup


category_cb_main = CallbackData('category', 'id', 'action')


def categories_markup_main():
    markup = InlineKeyboardMarkup()
    for idx, title in db.fetchall('SELECT * FROM categories'):
        markup.add(InlineKeyboardButton(title, callback_data=category_cb_main.new(id=idx, action='view')))

    return markup


add_basket_cb = CallbackData('product', 'id', 'action')


def add_basket(idx):
    markup = InlineKeyboardMarkup(resize_keyboard=True)
    markup.add(InlineKeyboardButton('Добавить в корзину', callback_data=add_basket_cb.new(id=idx, action='add_basket')))
    return markup
