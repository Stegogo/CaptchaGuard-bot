from aiogram import executor

from loader import bot
from utils.notify_admins import on_startup_notify

async def on_startup(dispatcher):
    await on_startup_notify(dispatcher)

async def on_shutdown(dispatcher):
    await bot.close()

if __name__ == '__main__':
    from commhandlers import dp
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)
