from buttons.users.dylevery import categories_markup_main, category_cb_main
from config import dp, bot, db
from aiogram import types
from buttons.users.main import main
from aiogram.types import ChatActions


async def show_products_main_menu(m, products, status):
    if len(products) == 0:
        await m.answer('Здесь ничего нет 😢')

        await bot.send_chat_action(m.chat.id, ChatActions.TYPING)
    else:
        for idx, title, body, image, price, _, _ in products:
            for id, stat in status:
                if idx in id and stat in 'start':
                    text = f'<b>{title}</b>\n\n{body}'
                    if image:
                        await m.answer_photo(photo=image,
                                             caption=text)
                    else:
                        await m.answer(text=text)


@dp.message_handler(text='📖 Меню')
async def catalog_menu(message: types.Message):
    await message.answer('Что вас интересует?', reply_markup=categories_markup_main())


@dp.callback_query_handler(category_cb_main.filter(action='view'))
async def menu_dyl(call: types.CallbackQuery, callback_data: dict):
    products = db.fetchall('''SELECT * FROM products
        WHERE products.tag = (SELECT title FROM categories WHERE idx=?)''',
                           (callback_data['id'],))
    status = db.fetchall("SELECT * FROM status")
    await show_products_main_menu(call.message, products, status)


@dp.message_handler(text='👈 Назад')
async def back(message: types.Message):
    await message.answer('Переход на главное меню', reply_markup=main())
