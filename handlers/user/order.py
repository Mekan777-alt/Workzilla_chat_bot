from aiogram import types
from aiogram import Router, F
from sqlalchemy.future import select
from context.user.order import UserOrder
from aiogram.fsm.context import FSMContext
from config import db_session
from data.base import User, Products
from buttons.user.main import CallbackDataCategoryOrder, category_order_markup, add_basket

router = Router()


@router.message(F.text == 'Заказать')
async def catalog_products(message: types.Message):
    await message.answer("Выберите категорию", reply_markup=category_order_markup())


@router.callback_query(CallbackDataCategoryOrder.filter())
async def product_order(call: types.CallbackQuery, callback_data: CallbackDataCategoryOrder):
    try:

        products = db_session.scalars(select(Products).where(Products.category_id == int(callback_data.action)))

        for product in products:
            await call.message.answer(f"{product.name}\n\n"
                                      f"Цена: {product.price}", reply_markup=add_basket(product.id))

    except Exception as e:
        print(e)


@router.message(F.text == 'Оформить заказ')
async def order_start(message: types.Message, state: FSMContext):
    await message.answer("Введите ваше имя")
    await state.set_state(UserOrder.user_name)


@router.message(UserOrder.user_name)
async def set_name(message: types.Message, state: FSMContext):
    await state.update_data(user_name=message.text)
    await message.answer("Введите марку автомобиля")
    await state.set_state(UserOrder.brand_auto)


@router.message(UserOrder.brand_auto)
async def set_brand_auto(message: types.Message, state: FSMContext):
    await state.update_data(brand_auto=message.text)
    await message.answer("Введите цвет автомобиля")
    await state.set_state(UserOrder.color_auto)


@router.message(UserOrder.color_auto)
async def set_color_auto(message: types.Message, state: FSMContext):
    await state.update_data(color_auto=message.text)
    await message.answer("Введите  гос. номер автомобиля")
    await state.set_state(UserOrder.number_auto)


@router.message(UserOrder.number_auto)
async def set_number_auto(message: types.Message, state: FSMContext):
    await state.update_data(number_auto=message.text)
    data = await state.get_data()
    user = User(
        user_id=message.from_user.id,
        name=data['user_name'],
        auto_brand=data['brand_auto'],
        color_auto=data['color_auto'],
        gos_number=data['number_auto']
    )
    db_session.add(user)
    db_session.commit()
    await message.answer("Принято!")
