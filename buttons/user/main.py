from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData
from config import db_session
from data.base import Category
from sqlalchemy.future import select
from aiogram.utils.keyboard import InlineKeyboardBuilder


def main_markup():
    button = [
        [KeyboardButton(text='Каталог')],
        [KeyboardButton(text='Заказать')]
    ]

    reply_markup = ReplyKeyboardMarkup(keyboard=button, resize_keyboard=True)

    return reply_markup


class CallbackDataCategory(CallbackData, prefix='category'):
    data: str
    action: int


def category_markup():
    builder = InlineKeyboardBuilder()
    try:

        category = db_session.scalars(select(Category))
        for category_obj in category:
            builder.button(
                text=str(category_obj.name), callback_data=CallbackDataCategory(data=str(category_obj.name),
                                                                                action=int(category_obj.id))
            )
        builder.adjust(1)
        return builder.as_markup()

    except Exception as e:

        return None


class CallbackDataCategoryOrder(CallbackData, prefix='category_order'):
    data: str
    action: int


def category_order_markup():
    builder = InlineKeyboardBuilder()
    try:

        category = db_session.scalars(select(Category))
        for category_obj in category:
            builder.button(
                text=str(category_obj.name), callback_data=CallbackDataCategoryOrder(data=str(category_obj.name),
                                                                                     action=int(category_obj.id))
            )
        builder.adjust(1)
        return builder.as_markup()

    except Exception as e:

        return None


def add_basket(product_id):
    button = [
        [InlineKeyboardButton(text='Добавить в корзину', callback_data=f'add_basket_{product_id}')]
    ]
    markup = InlineKeyboardMarkup(inline_keyboard=button)
    return markup