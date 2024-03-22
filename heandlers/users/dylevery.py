from datetime import datetime
from aiogram.types import ChatActions
from buttons.users.dylevery import product_markup, categories_markup, menu_markup, category_cb, product_cb, add_basket, add_basket_cb
from config import dp, db, bot
from aiogram import types


def time_dlv():
    current_time = str(datetime.now().time())
    return current_time


@dp.message_handler(text='🎒 Заказать')
async def cmd_dyl(message: types.Message):
    db.query("INSERT INTO regime VALUES (?, ?)", (0, 1))
    await message.answer("При заказе от 5000 рублей 2% скидка", reply_markup=menu_markup())
    await message.answer("ВЫБЕРИТЕ РАЗДЕЛ", reply_markup=categories_markup())


@dp.message_handler(text='📖 МЕНЮ')
async def menu_dyl(message: types.Message):
    await message.answer("Выберите раздел", reply_markup=categories_markup())


@dp.callback_query_handler(category_cb.filter(action='view_2'))
async def menu_dyl(call: types.CallbackQuery, callback_data: dict):
    products = db.fetchall('''SELECT * FROM products
        WHERE products.tag = (SELECT title FROM categories WHERE idx=?)''',
                           (callback_data['id'],))
    status = db.fetchall("SELECT * FROM status")
    await show_products(call.message, products, status)


@dp.callback_query_handler(add_basket_cb.filter(action='add_basket'))
async def add_basket_filter(call: types.CallbackQuery, callback_data: dict):
    product = db.fetchone('''SELECT * FROM products where idx=?''', (callback_data['id'],))

    if product[-1] is not None:
        await call.message.edit_reply_markup(product_markup(callback_data['id'], 'meshok'))
    else:
        await call.message.edit_reply_markup(product_markup(callback_data['id']))


@dp.callback_query_handler(product_cb.filter(action=['add', 'add_meshok', 'add_kg']))
async def add_product_callback_handler(query: types.CallbackQuery, callback_data: dict):
    product_id = callback_data['id']
    action = callback_data['action']

    if action.startswith('add_'):
        prefix = action.split('_')[1]
        if prefix == 'meshok':
            quantity = db.fetchone('''SELECT bag_weight FROM products where idx=?''', (product_id, ))
            db.query(f'INSERT INTO cart VALUES (?, ?, ?, null, null, null, null, null, null)',
                     (query.message.chat.id, product_id, quantity[0]))
            await query.answer('Товар добавлен в корзину!')
            await query.message.delete()
        elif prefix == 'kg':
            db.query('INSERT INTO cart VALUES (?, ?, 1, null, null, null, null, null, null)',
                     (query.message.chat.id, product_id))
            await query.answer('Товар добавлен в корзину!')
            await query.message.delete()

    else:
        db.query('INSERT INTO cart VALUES (?, ?, 1, null, null, null, null, null, null)',
                (query.message.chat.id, product_id))
        await query.answer('Товар добавлен в корзину!')
        await query.message.delete()


async def show_products(m, products, status):
    if len(products) == 0:
        await m.answer('Здесь ничего нет 😢')

        await bot.send_chat_action(m.chat.id, ChatActions.TYPING)
    else:
        for idx, title, body, image, price, _, _ in products:
            for id, stat in status:
                if idx in id and stat in 'start':
                    # markup = product_markup(idx, price)
                    markup = add_basket(idx)
                    text = f'<b>{title}</b>\n\n{body}'
                    if image:
                        await m.answer_photo(photo=image,
                                             caption=text,
                                             reply_markup=markup)
                    else:
                        await m.answer(text=text, reply_markup=markup)


