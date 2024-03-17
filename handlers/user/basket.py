from aiogram import types, F, Router
from sqlalchemy.future import select
from config import db_session
from sqlalchemy import delete
from data.base import Basket, Products
from buttons.user.main import delete_product_from_basket, CallbackDataRemoveBasket

router = Router()


@router.message(F.text == '👉 Корзина')
async def set_basket(message: types.Message):
    try:
        basket = db_session.scalars(select(Basket).where(Basket.user_id == int(message.from_user.id)))

        for bas in basket:
            product = db_session.scalar(select(Products).where(Products.id == bas.product_id))

            await message.answer(f"Название продукта: {product.name} \n\n"
                                 f"Цена: {product.price} \n\n", reply_markup=delete_product_from_basket(product.id))

    except Exception as e:

        print(e)


@router.callback_query(CallbackDataRemoveBasket.filter())
async def remove_product_from_basket(call: types.CallbackQuery, callback_data: CallbackDataRemoveBasket):
    try:

        db_session.execute(delete(Basket).where(Basket.product_id == callback_data.id))
        db_session.commit()

        await call.answer("Товар удален из корзины")
        await call.message.delete()


    except Exception as e:

        print(e)
