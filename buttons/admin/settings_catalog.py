from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
from config import db
from aiogram.utils.callback_data import CallbackData

category_cb = CallbackData('category', 'id', 'action')


def catalog():
    markup = InlineKeyboardMarkup()
    for idx, title in db.fetchall('SELECT * FROM categories'):
        markup.add(InlineKeyboardButton(title, category_cb.new(id=idx, action='view')))

    markup.add(InlineKeyboardButton('+ Добавить категорию', callback_data='add_category'))
    return markup


def back_markup():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add('👈 Назад')

    return markup


def check_markup():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.row('👈 Назад', '✅ Продолжить')

    return markup


def confirm_markup():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add('✅ Подтвердить заказ')

    return markup
