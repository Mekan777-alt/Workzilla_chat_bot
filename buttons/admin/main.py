from aiogram.filters.callback_data import CallbackData
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
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


class CallbackAdminDataCategory(CallbackData, prefix='categoryAdmin'):
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


class CallbackAdminDataCategoryOrder(CallbackData, prefix='category_orderAdmin'):
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


class  CallbackAdminDataProduct(CallbackData, prefix='productAdmin'):
    data: str
    id: int


def product_markup(product):
    builder = InlineKeyboardBuilder()
    try:
        # products = db_session.scalars(select(Products)).where(Products.category_id == int(callback_data.action)))
        builder.button(
            text=str("Удалить продукт"), callback_data=CallbackAdminDataProduct(data=str(product.name),
                                                                                id=int(product.id))
        )
        builder.adjust(1)
        return builder.as_markup()

    except Exception as e:

        return None


class CallbackAdminNewProduct(CallbackData, prefix='new_product_admin'):
    data: str


def new_category_markup():
    button = [
        [KeyboardButton(text='Добавить категорию')],
        [KeyboardButton(text='Назад')]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard=button, resize_keyboard=True)

    return reply_markup

def new_product_markup():
    button = [
        [KeyboardButton(text='Добавить продукт')],
        [KeyboardButton(text='Назад')]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard=button, resize_keyboard=True)

    return reply_markup
