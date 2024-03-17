from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from buttons.admin.main import main_markup
from config import db_session
from context.admin.product import ProductState
from data.base import Products

router = Router()


@router.message(F.text == '👉 Добавить продукт')
async def add_product(message: types.Message, state: FSMContext):
    await message.answer("Введите наименование: ", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(ProductState.name)


@router.message(ProductState.name)
async def set_product_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Введите цену: ")
    await state.set_state(ProductState.price)


@router.message(ProductState.price)
async def set_product_price(message: types.Message, state: FSMContext):
    await state.update_data(price=message.text)
    data = await state.get_data()

    try:
        product = Products(
            category_id=data["category_id"],
            name=data["name"],
            price=data["price"]
        )

        db_session.add(product)
        db_session.commit()

        await message.answer('Продукт добавлен в категорию', reply_markup=main_markup())

    except Exception as e:

        print(e)

# @router.callback_query(CallbackAdminNewProduct.filter())
# async def new_product(call: types.CallbackQuery, callback_data: CallbackAdminNewProduct):
# try:

# product = Products(
# id=callback_data.id,
# cate=call.from_user.id
# )
