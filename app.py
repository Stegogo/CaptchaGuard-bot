from aiogram import executor

if __name__ == '__main__':
    from commhandlers import dp

    executor.start_polling(dp, on_startup=main.on_startup, on_shutdown=main.on_shutdown)
