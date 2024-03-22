from config import dp, db, bot, SUPPORT_CHAT
from aiogram import types
from buttons.users.sos import sos
from context.context import SosState
from aiogram.dispatcher import FSMContext
from buttons.users.reserved import phone_number
from buttons.users.main import main
from buttons.users.reserved import done_or_cancel
from aiogram.types import ContentType


@dp.message_handler(text='? Помощь')
async def sos_cmd(message: types.Message):
    await message.answer("Выберите способ", reply_markup=sos())


@dp.message_handler(text="📞 Позвонить")
async def command_phone(message: types.Message):
    await message.answer("Пожалуйста свяжитесь с нами по номеру телефона\n"
                         "тут номер телефона")


@dp.message_handler(text="✉ Написать сообщение")
async def write_sms(message: types.Message):
    await SosState.question.set()
    await message.answer('В чем суть проблемы? Опишите как можно детальнее и администратор обязательно вам ответит.',
                         reply_markup=sos())


@dp.message_handler(state=SosState.question)
async def process_qua(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text != '👈 Назад':
            data['question'] = message.text
            await message.answer("Введите номер телефона пожалуйста.", reply_markup=phone_number())
            await SosState.next()
        else:
            await message.answer('Отменено!', reply_markup=main())
            await state.finish()


@dp.message_handler(state=SosState.phone_number)
async def process_phn(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['phone_number'] = message.text
        await SosState.next()
        await message.answer('Убедитесь, что все верно.', reply_markup=done_or_cancel())


@dp.message_handler(content_types=ContentType.CONTACT, state=SosState.phone_number)
async def process_cnt(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['phone_number'] = message.contact['phone_number']
        await SosState.next()
        await message.answer('Убедитесь, что все верно.', reply_markup=done_or_cancel())


@dp.message_handler(lambda message: message.text not in ["✅ Верно", "❌ Нет"], state=SosState.submit)
async def process_invalid(message: types.Message):
    await message.answer('Такого варианта не было.')


@dp.message_handler(text="❌ Нет", state=SosState.submit)
async def process_not(message: types.Message, state: FSMContext):
    await message.answer('Отменено!', reply_markup=main())
    await state.finish()


@dp.message_handler(text="✅ Верно", state=SosState.submit)
async def process_done(message: types.Message, state: FSMContext):
    cid = message.chat.id
    async with state.proxy() as data:
        db.query('INSERT INTO questions VALUES (?, ?)',
                 (cid, data['question']))
        await message.answer('Отправлено!', reply_markup=main())
        await bot.send_message(SUPPORT_CHAT, "SOS\n"
                                             "\n"
                                             f"Вопрос: {data['question']}\n"
                                             f"Номер телефона отправителя: {data['phone_number']}")

    await state.finish()
