import aiogram.types
from aiogram import executor, types
from types import User
from utils.notify_admins import on_startup_notify, on_shutdown_notify
from loader import bot
import os
import psycopg2

async def on_startup(dispatcher):
    await on_startup_notify(dispatcher)

async def on_shutdown(dispatcher):
    await on_shutdown_notify(dispatcher)
    await bot.close()


async def get_lang():
    from commhandlers import database
    if types.User.get_current().id != types.Chat.get_current().id:
        try:
            return await database.get_lang(types.Chat.get_current().id)
        except AttributeError:
            return "en"
    else:
        if types.User.get_current().language_code in ['en', 'ru', 'uk']:
            return types.User.get_current().language_code
        else:
            return 'en'

if __name__ == '__main__':
    from commhandlers import dp
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)
