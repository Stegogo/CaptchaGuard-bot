import logging

from aiogram import Dispatcher, Bot
from data.config import ADMINS, TOKEN

async def on_startup_notify(dp: Dispatcher):
    bot = Bot(token=TOKEN)
    try:
        await dp.bot.send_message(ADMINS, f"Бот запущен.")

    except Exception as err:
        logging.exception(err)
async def on_shutdown_notify(dp: Dispatcher):
    bot = Bot(token=TOKEN)
    try:
        await dp.bot.send_message(ADMINS, f"Бот упал.")

    except Exception as err:
        logging.exception(err)
