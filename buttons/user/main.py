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


class CallbackDataAddBasket(CallbackData, prefix='add_basket'):
    id: int
    action: str


def add_basket(product_id, price):
    builder = InlineKeyboardBuilder()

    builder.button(
        text=f"Заказать за - {price}₽", callback_data=CallbackDataAddBasket(id=product_id, action='add')
    )
    return builder.as_markup()


def order_markup():
    buttons = [
        [KeyboardButton(text='Меню'), KeyboardButton(text='Оформить заказ')],
        [KeyboardButton(text='Корзина')],
    ]

    markup = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=buttons)

    return markup


class CallbackDataRemoveBasket(CallbackData, prefix='remove_basket'):
    id: int
    action: str


def delete_product_from_basket(product_id):

    builder = InlineKeyboardBuilder()

    builder.button(
        text='Удалить из корзины', callback_data=CallbackDataRemoveBasket(id=product_id, action='remove')
    )

    return builder.as_markup()


def back_order():
    button = [
        [KeyboardButton(text='Назад')]
    ]
    markup = ReplyKeyboardMarkup(keyboard=button, resize_keyboard=True)
    return markup
