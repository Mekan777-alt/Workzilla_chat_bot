import os

from config import dp
from aiogram import types
from context.context import Admin
from buttons.admin.admin import admin
from aiogram.dispatcher import FSMContext
from dotenv import load_dotenv

load_dotenv()

login = os.getenv('ADMIN_LOGIN')
password = os.getenv('ADMIN_PASSWORD')


@dp.message_handler(commands='admin', state=None)
async def start_admin(message: types.Message):
    await Admin.login.set()
    await message.answer('Введите логин: ')


@dp.message_handler(text=login, state=Admin.login)
async def set_password(message: types.Message):
    if message.text in login:
        await Admin.next()
        await message.answer('Пароль: ')


@dp.message_handler(lambda message: message.text is not login, state=Admin.login)
async def restart_login(message: types.Message):
    await message.answer('Неверный логин, повторите')


@dp.message_handler(text=password, state=Admin.password)
async def set_password(message: types.Message, state: FSMContext):
    if message.text in password:
        await message.answer('Включен режим администратора', reply_markup=admin())
    await state.finish()


@dp.message_handler(lambda message: message.text is not password, state=Admin.password)
async def restart_password(message: types.Message):
    await message.answer('Неверный пароль, повторите')
