import asyncio
import random
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from asyncpg import Connection, Record
import commhandlers

from loader import bot, dp, db

lang = None
greet = None
protect = True

@dp.message_handler(commands="menu")
async def send_menu(message: types.Message):
    text = f"""
Привет! 👋 Я - капчабот, защищаю ваш чат от пользователей-ботов.\n
Вы вызвали моё меню настроек.
Пользоваться им могут только администраторы чата.\n
Доступные команды:
/set_language: Сменить язык 🌍
/set_greeting: Сменить приветствие ⭐️
/disable_captcha: Отключить капчу 🔓
/enable_captcha: Включить капчу 🔒"""
    await message.answer(text=text)

@dp.message_handler(commands="set_greeting")
async def set_greet_1(message: types.Message):
    text = f"""
Вы можете настроить сообщение, которое будет приветствовать новых участников чата после того, как они прошли капчу.
Например, вы можете оставить ссылку на правила вашего чата или на другие важные материалы.\n
Пожалуйста, введите новое сообщение приветствия после команды, вот так:
/set_new_greeting Привет, $user, мы рады тебя видеть!\n
Вы также можете отключить приветствие:
/set_new_greeting Отключить 
"""
    await message.answer(text=text)

@dp.message_handler(commands=['set_new_greeting'])
async def set_greet_2(message: types.Message):
    arguments = message.get_args()
    if arguments == 'Отключить':
        await commhandlers.database.set_new_greeting(message.chat.id, " ")
    else:
        await commhandlers.database.set_new_greeting(message.chat.id, arguments)
    await message.answer("Сообщение приветствия изменено!")

@dp.message_handler(commands=['disable_captcha'])
async def set_greet_2(message: types.Message):
    mode = await commhandlers.database.get_protect(message.chat.id)
    if mode == 'True':
        await commhandlers.database.set_new_protect(message.chat.id, "False")
        await message.answer("Капча отключена! 🔓 Если хотите вернуть её обратно, введите /enable_captcha")
    else:
        await message.answer("Капча уже отключена! 🔓")
@dp.message_handler(commands=['enable_captcha'])
async def set_greet_2(message: types.Message):
    mode = await commhandlers.database.get_protect(message.chat.id)
    if mode == 'False':
        await commhandlers.database.set_new_protect(message.chat.id, "True")
        await message.answer("Капча включена! 🔒 Если хотите выключить её, введите /disable_captcha")
    else:
        await message.answer("Капча уже включена! 🔒")
