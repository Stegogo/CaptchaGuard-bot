import aiogram.types
from aiogram import executor, types
from utils.notify_admins import on_startup_notify
from loader import bot

async def on_startup(dispatcher):
    await on_startup_notify(dispatcher)

async def on_shutdown(dispatcher):
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
    import os

    PORT = int(os.environ.get('PORT', 5000))
    executor.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path="1858575777:AAExROkiyWg7w0JXpazthxt3Qjup8w8F5ZA")
    executor.bot.setWebhook('https://captcha-guard-bot.herokuapp.com/' + TOKEN)
    executor.idle()
    #executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)
