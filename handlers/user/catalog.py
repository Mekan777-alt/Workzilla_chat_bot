import asyncio
from config import db_session
from aiogram import types, Router, F
from buttons.user.main import category_markup, CallbackDataCategory, main_markup
from sqlalchemy.future import select
from data.base import Products

router = Router()


@router.message(F.text == '👉 Каталог')
async def catalog(message: types.Message):
    await message.answer("Выберите категорию", reply_markup=category_markup())


@router.callback_query(CallbackDataCategory.filter())
async def filter_category(call: types.CallbackQuery, callback_data: CallbackDataCategory):
    try:
        products = db_session.scalars(select(Products).where(Products.category_id == int(callback_data.action)))

        for product in products:
            if product is not None:
                await call.message.answer(f"{product.name}\n\n"
                                          f"Цена: {product.price}", reply_markup=main_markup())
                await asyncio.sleep(1)

            else:
                await call.message.edit_text("По данной категории нет товаров", reply_markup=main_markup())
    except Exception as e:
        print(e)
