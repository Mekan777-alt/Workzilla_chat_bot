import asyncio
import os
from service.generateFile import create_product_receipt
from datetime import datetime
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message, ChatActions, ReplyKeyboardMarkup, CallbackQuery, \
    InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ContentType
from buttons.users.main import main
from config import dp, db, bot, DELIVERY_CHAT
from buttons.admin.settings_catalog import check_markup, confirm_markup
# from hendlers.user.dostavka import dyl_start, projarkas, garnishs, sauces
from aiogram.utils.callback_data import CallbackData
from heandlers.users.dylevery import cmd_dyl
import json

b54 = KeyboardButton("📞 Отправить свой номер", request_contact=True)
send_phone = ReplyKeyboardMarkup(resize_keyboard=True).add(b54)

dostavka = "🎒 Доставка"
samovyvoz = "🚗 Самовывоз"

product_cb_2 = CallbackData('product', 'id', 'action')


def product_markup_2(idx, count):
    global product_cb_2

    markup = InlineKeyboardMarkup()
    back_btn = InlineKeyboardButton('➖', callback_data=product_cb_2.new(id=idx, action='decrease'))
    count_btn = InlineKeyboardButton(count, callback_data=product_cb_2.new(id=idx, action='count'))
    next_btn = InlineKeyboardButton('➕️', callback_data=product_cb_2.new(id=idx, action='increase'))

    markup.row(back_btn, count_btn, next_btn)

    return markup


def device_():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    yes = "Да"
    not_ = "Нет"
    markup.add(yes, not_)
    return markup


def device_count():
    markup = ReplyKeyboardMarkup()
    for i in range(1, 6):
        i = str(i)
        markup.add(i)

    return markup


@dp.message_handler(text='🛒 Перейти в Корзину')
async def process_cart(message: types.Message, state: FSMContext):
    cart_data = db.fetchall(
        'SELECT * FROM cart WHERE cid=?', (message.chat.id,))
    if len(cart_data) == 0:
        await message.answer('Ваша корзина пуста.')
    else:
        await bot.send_chat_action(message.chat.id, ChatActions.TYPING)
        async with state.proxy() as data:
            data['products'] = {}
        order_cost = 0

        for _, idx, count_in_cart, comment, projarka, garnish, sauce, amount, spice in cart_data:
            product = db.fetchone('SELECT * FROM products WHERE idx=?', (idx,))
            if product is None:
                db.query('DELETE FROM cart WHERE idx=?', (idx,))
            else:
                _, title, body, image, price, _, _, _ = product

                markup = product_markup_2(idx, count_in_cart)
                text = f'<b>{title}</b>\n'
                info = ""

                if image:
                    await message.answer_photo(photo=image,
                                               caption=text,
                                               reply_markup=markup)
                else:
                    await message.answer(text=text, reply_markup=markup)

                order_cost += price
                async with state.proxy() as data:
                    if data['products'].get(idx):
                        idx += "2"

                    data['products'][idx] = [title, price, count_in_cart, info]

        if order_cost != 0:
            markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
            markup.add('📦 Оформить заказ', "🗑 Очистить корзину").add('👈 Назад')

            await message.answer('Отличный выбор, теперь эти позиции в корзине.\n'
                                 'Нажмите на кнопки оформить заказ или назад',
                                 reply_markup=markup)


@dp.message_handler(text='👈 Назад')
async def back_menu(message: types.Message):
    await cmd_dyl(message)


@dp.callback_query_handler(product_cb_2.filter(action=['count', 'increase', 'decrease']))
async def product_callback_handler(query: CallbackQuery, callback_data: dict, state: FSMContext):
    idx = callback_data['id']
    action = callback_data['action']
    if 'count' == action:
        async with state.proxy() as data:
            if 'products' not in data.keys():
                await process_cart(query.message, state)
            else:
                await query.answer(f'Количество - {data["products"][idx][2]}')
    else:
        async with state.proxy() as data:
            if 'products' not in data.keys():
                await process_cart(query.message, state)
            else:
                data['products'][idx][2] += 1 if 'increase' == action else -1
                count_in_cart = data['products'][idx][2]
                if count_in_cart <= 0:
                    db.query('''DELETE FROM cart
                    WHERE cid = ? AND idx = ?''', (query.message.chat.id, idx))
                    await query.message.delete()
                else:
                    db.query('''UPDATE cart
                        SET quantity = ?
                    WHERE cid = ? AND idx = ?''', (count_in_cart, query.message.chat.id, idx))
                    await query.message.edit_reply_markup(product_markup_2(idx, count_in_cart))


class CheckoutState(StatesGroup):
    check_cart = State()
    name = State()
    brand_auto = State()
    color_auto = State()
    number_auto = State()
    confirm = State()


@dp.message_handler(text="🗑 Очистить корзину")
async def delete_cart(message: types.Message):
    db.query("""DELETE FROM cart WHERE cid=?""", (message.chat.id,))
    await message.answer("Готово", reply_markup=main())


@dp.message_handler(text='📦 Оформить заказ')
async def process_checkout(message: Message, state: FSMContext):
    async with state.proxy() as data:
        total_price = 0
        for title, price, count_in_cart, info in data['products'].values():
            tp = count_in_cart * price
            total_price += tp

        await CheckoutState.check_cart.set()
        await checkout(message, state)


async def checkout(message, state):
    global MESSAGE
    answer = ''
    total_price = 0
    discount_applied = False

    async with state.proxy() as data:
        for title, price, count_in_cart, info in data['products'].values():
            if count_in_cart > 0:
                tp = count_in_cart * price
                answer += f'<b>{title}</b> * {count_in_cart}кг/шт. = {tp}₽\n'
                total_price += tp

        if total_price > 5000:
            discount = total_price * 0.02  # Скидка 2%
            total_price -= discount
            discount_applied = True

    if discount_applied:
        await message.answer(f'{answer}\nОбщая сумма заказа: {total_price}₽ (Скидка 2% применена).',
                             reply_markup=check_markup())
    else:
        await message.answer(f'{answer}\nОбщая сумма заказа: {total_price}₽.',
                             reply_markup=check_markup())


@dp.pre_checkout_query_handler()
async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    print('order_info')
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@dp.message_handler(lambda message: message.text not in ['✅ Все верно', '👈 Назад'],
                    state=CheckoutState.check_cart)
async def process_check_cart_invalid(message: Message):
    await message.reply('Такого варианта не было.')


@dp.message_handler(text='👈 Назад', state=CheckoutState.check_cart)
async def process_check_cart_back(message: types.Message, state: FSMContext):
    await state.finish()
    await process_cart(message, state)


@dp.message_handler(text='👈 Назад', state=CheckoutState.name)
async def process_name_back(message: Message, state: FSMContext):
    await CheckoutState.check_cart.set()
    await checkout(message, state)


@dp.message_handler(text='✅ Все верно', state=CheckoutState.check_cart)
async def dylevery(message: types.Message, state: FSMContext):
    await CheckoutState.name.set()
    await message.answer('Укажите свое имя.', reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(state=CheckoutState.name)
async def process_name(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text

        await CheckoutState.brand_auto.set()
        await message.answer("Укажите марку машины")

        # await CheckoutState.next()


@dp.message_handler(state=CheckoutState.brand_auto)
async def process_brand(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['brand_auto'] = message.text

        await CheckoutState.color_auto.set()
        await message.answer("Укажите цвет машины")
        # await CheckoutState.next()


@dp.message_handler(state=CheckoutState.color_auto)
async def process_color_auto(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['color_auto'] = message.text

        await CheckoutState.number_auto.set()
        await message.answer("Укажите гос. номер автомобиля")
        # await CheckoutState.next()


@dp.message_handler(state=CheckoutState.number_auto)
async def process_auto_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['number_auto'] = message.text

    await CheckoutState.confirm.set()
    await confirm(message, state)
    # await CheckoutState.next()


async def confirm(message, state):
    async with state.proxy() as data:
        total_price = 0
        an = ''
        discount_applied = False

        for title, price, count_in_cart, info in data['products'].values():
            if count_in_cart > 0:
                tp = count_in_cart * price
                an += f'<b>{title}</b> - {count_in_cart}кг/шт\n{info}\n\n'
                total_price += tp

        if total_price > 5000:
            discount = total_price * 0.02  # Скидка 2%
            total_price -= discount
            discount_applied = True

        text = f"Убедитесь, что все правильно оформлено и подтвердите заказ.\n\n" \
               f"<b>Данные заказа</b>\n" \
               f"Получатель: {data['name']}\n" \
               f"Цвет машины: {data['color_auto']}\n" \
               f"Марка машины: {data['brand_auto']}\n" \
               f"Номер машины: {data['number_auto']}\n" \

        if discount_applied:
            text += f"Общая стоимость: {total_price} рублей (Скидка 2% применена)\n\n" \
                    f"Ваш заказ:\n{an}"
        else:
            text += f"Общая стоимость: {total_price} рублей\n\n" \
                    f"Ваш заказ:\n{an}"

        await message.answer(text, reply_markup=confirm_markup())


@dp.message_handler(lambda message: message.text not in ['✅ Подтвердить заказ', '👈 Назад'],
                    state=CheckoutState.confirm)
async def process_confirm_invalid(message: Message):
    await message.reply('Такого варианта не было.')


@dp.message_handler(text='✅ Подтвердить заказ', state=CheckoutState.confirm)
async def process_confirm(message: Message, state: FSMContext):
    async with state.proxy() as data:
        await message.answer("Заказ успешно создан\n\n"
                             "Ниже приложен чек")

        doc = await create_product_receipt(state, message.from_user.id)

        doc_path = open(doc, 'rb+')
        await bot.send_message(-4177653235, text=f"Детали заказа\n\n"
                                                 f"Получатель: {data['name']}\n"
                                                 f"Цвет машины: {data['color_auto']}\n"
                                                 f"Марка машины: {data['brand_auto']}\n"
                                                 f"Номер машины: {data['number_auto']}\n")
        await bot.send_document(-4177653235, document=doc_path)

        db.query('DELETE FROM CART WHERE cid=?', (message.from_user.id,))
        os.remove(doc)
        await state.finish()
