import logging

from aiogram import Dispatcher, Bot, types
from data.config import ADMINS, TOKEN


async def on_startup_notify(dp: Dispatcher):
    bot = Bot(token=TOKEN)
    try:
        await dp.bot.send_message(ADMINS, f"Привет! Бот запущен.")

    except Exception as err:
        logging.exception(err)
