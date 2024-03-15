from aiogram.filters.callback_data import CallbackData
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.future import select

from config import db_session
from data.base import Category


def main_markup():
    button = [
        [KeyboardButton(text='Изменить категорию')],
        [KeyboardButton(text='Добавить категорию')]
    ]

    reply_markup = ReplyKeyboardMarkup(keyboard=button, resize_keyboard=True)

    return reply_markup


class CallbackAdminDataCategory(CallbackData, prefix='category'):
    data: str
    action: int


def category_markup():
    builder = InlineKeyboardBuilder()
    try:

        category = db_session.scalars(select(Category))
        for category_obj in category:
            builder.button(
                text=str(category_obj.name), callback_data=CallbackAdminDataCategory(data=str(category_obj.name),
                                                                                     action=int(category_obj.id))
            )
        builder.adjust(1)
        return builder.as_markup()

    except Exception as e:

        return None


class CallbackAdminDataCategoryOrder(CallbackData, prefix='category_order'):
    data: str
    action: int


def category_order_markup():
    builder = InlineKeyboardBuilder()
    try:

        category = db_session.scalars(select(Category))
        for category_obj in category:
            builder.button(
                text=str(category_obj.name), callback_data=CallbackAdminDataCategoryOrder(data=str(category_obj.name),
                                                                                          action=int(category_obj.id))
            )
        builder.adjust(1)
        return builder.as_markup()

    except Exception as e:

        return None

