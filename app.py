from aiogram import executor
from utils.notify_admins import on_startup_notify, on_shutdown_notify

if __name__ == '__main__':
    from commhandlers import dp

    executor.start_polling(dp, on_startup=on_startup_notify, on_shutdown=on_shutdown_notify)
