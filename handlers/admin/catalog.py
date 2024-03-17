from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from sqlalchemy import delete
from sqlalchemy.future import select

from buttons.admin.main import category_markup, CallbackAdminDataCategory, main_markup, product_markup, \
    CallbackAdminDataProduct, new_product_markup
from config import db_session
from context.admin.category import CategoryState
from context.admin.product import ProductState
from data.base import Products, Category

router = Router()


@router.message(F.text == '👉 Изменить категорию')
async def catalog(message: types.Message, state: FSMContext):
    await message.answer("Выберите категорию", reply_markup=category_markup())
    await state.set_state(ProductState.category_id)


@router.callback_query(CallbackAdminDataCategory.filter(), ProductState.category_id)
async def filter_category(call: types.CallbackQuery, callback_data: CallbackAdminDataCategory, state: FSMContext):
    try:
        products = db_session.scalars(select(Products).where(Products.category_id == int(callback_data.action)))

        existing_product_messages = []

        await call.message.answer(" Выберите действие ниже", reply_markup=new_product_markup())

        await state.update_data(category_id=callback_data.action)

        for product in products:
            if product is not None:
                message = f"{product.name}\n\nЦена: {product.price}"
                markup = product_markup(product)
                existing_product_messages.append((message, markup))

        if existing_product_messages:
            for message, markup in existing_product_messages:
                await call.message.answer(message, reply_markup=markup)
        else:
            await call.message.edit_text("По данной категории нет товаров", reply_markup=main_markup())


    except Exception as e:
        print(e)


@router.callback_query(CallbackAdminDataProduct.filter())
async def remove_product(call: types.CallbackQuery, callback_data: CallbackAdminDataProduct):
    try:

        db_session.execute(delete(Products).where(Products.id == callback_data.id))
        db_session.commit()

        await call.answer("Продукт удален", reply_markup=main_markup())
        await call.message.delete()


    except Exception as e:

        print(e)


@router.message(F.text == '👉 Добавить категорию')
async def catalog(message: types.Message, state: FSMContext):
    await message.answer("Введите наименование: ", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(CategoryState.name)


@router.message(CategoryState.name)
async def set_category_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    data = await state.get_data()

    try:
        category = Category(
            name=data["name"],
        )

        db_session.add(category)
        db_session.commit()

        await message.answer('Продукт добавлен в категорию', reply_markup=main_markup())

    except Exception as e:

        print(e)
