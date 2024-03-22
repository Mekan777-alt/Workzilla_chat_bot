from config import dp, db
from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery


@dp.message_handler(text='⚙️ Настройка режима')
async def regime_settings(message: types.Message, edit=None):
    regime = db.fetchall('SELECT * FROM regime')[0]
    action = ['ДОСТАВКА']
    markup = InlineKeyboardMarkup()
    for idx, item in enumerate(regime):
        if item == 1:
            allowed = '✅'
        else:
            allowed = '❌'
        markup.add(InlineKeyboardButton(f"{action[idx]}{allowed}", callback_data=f"change_{idx}"))
    if edit:
        await message.edit_reply_markup(reply_markup=markup)
    else:
        await message.answer('Настройка режима:', reply_markup=markup)


@dp.callback_query_handler(text_contains="change_")
async def regime_callback_handler(query: CallbackQuery):
    regime = db.fetchall('SELECT * FROM regime')[0]
    column_id = int(query.data[7:])
    column = ""

    if column_id == 0:
        column = "bron"
    elif column_id == 1:
        column = "delivery"

    change_value = regime[column_id]
    if change_value == 1:
        to_change = 0
    else:
        to_change = 1

    db.query(f'''UPDATE regime SET {column} = {to_change}''')
    await regime_settings(query.message, edit=True)
    await query.answer("Настройки обновлены!")
