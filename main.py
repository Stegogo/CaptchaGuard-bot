from aiogram import executor, types
from utils.notify_admins import on_startup_notify
from loader import bot

async def on_startup(dispatcher):
    await on_startup_notify(dispatcher)

async def on_shutdown(dispatcher):
    await bot.close()

async def get_lang():
    from commhandlers import database
    try:
        return await database.get_lang(types.Chat.get_current().id)
    except AttributeError:
        return "en"

if __name__ == '__main__':
    from commhandlers import dp
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)
