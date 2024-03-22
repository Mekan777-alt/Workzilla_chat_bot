from buttons.users.dylevery import categories_markup_main, category_cb_main
from config import dp, bot, db
from aiogram import types
from buttons.users.main import main
from aiogram.types import ChatActions
from aiogram.utils.callback_data import CallbackData


async def show_products_main_menu(m, products, status):
    if len(products) == 0:
        await m.answer('Здесь ничего нет 😢')

        await bot.send_chat_action(m.chat.id, ChatActions.TYPING)
    else:
        for idx, title, body, image, price, _, _, _ in products:
            for id, stat in status:
                if idx in id and stat in 'start':
                    text = f'<b>{title}</b>\n\n{body}'
                    if image:
                        await m.answer_photo(photo=image,
                                             caption=text)
                    else:
                        await m.answer(text=text)


pod_category_cb = CallbackData('podcategory', 'id', 'action')


def show_pod_category(products):
    markup = types.InlineKeyboardMarkup()
    category = []
    for product in products:
        if product[7] in category:
            pass
        else:
            action_cat = product[7].split()
            markup.add(types.InlineKeyboardButton(text=product[7], callback_data=pod_category_cb.new(id=1, action=str(action_cat[0]))))
            category.append(product[7])
    return markup


@dp.message_handler(text='📖 Меню')
async def catalog_menu(message: types.Message):
    await message.answer('Что вас интересует?', reply_markup=categories_markup_main())


@dp.callback_query_handler(pod_category_cb.filter())
async def set_pod_category(call: types.CallbackQuery, callback_data: pod_category_cb):
    pod_category = db.fetchone("""SELECT pod_tag FROM products WHERE pod_tag LIKE ?""",
                               ('%' + callback_data['action'] + '%',))
    products = db.fetchall("""SELECT * FROM products WHERE pod_tag=?""", (pod_category[0],))
    for idx, title, body, image, price, _, _, _ in products:
        text = f'<b>{title}</b>\n\n{body}'
        if image:
            await call.message.answer_photo(photo=image,
                                            caption=text)
        else:
            await call.message.answer(text=text)


@dp.callback_query_handler(category_cb_main.filter(action='view'))
async def menu_dyl(call: types.CallbackQuery, callback_data: dict):
    products = db.fetchall('''SELECT * FROM products
        WHERE products.tag = (SELECT title FROM categories WHERE idx=?)''',
                           (callback_data['id'],))
    status = db.fetchall("SELECT * FROM status")
    if products[0][7] is not None:
        await call.message.edit_reply_markup(reply_markup=show_pod_category(products))
    else:
        await show_products_main_menu(call.message, products, status)


@dp.message_handler(text='👈 Назад')
async def back(message: types.Message):
    await message.answer('Переход на главное меню', reply_markup=main())
