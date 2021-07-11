import time

from aiogram.types import CallbackQuery
import commhandlers
from loader import bot, dp

@dp.callback_query_handler(lambda c: c.data == 'answer')
async def process_callback_button1(callback_query: CallbackQuery):
    if commhandlers.data.id == callback_query.from_user.id:
        await bot.answer_callback_query(callback_query.id)
        message_obj = await bot.send_message(callback_query.message.chat.id, 'Правильно!')
        if not commhandlers.success: commhandlers.success = True
        await delete_msg(callback_query.message, message_obj)
    else:
        await bot.answer_callback_query(
            callback_query.id,
            text='А это не для тебя 🤡', show_alert=True)


@dp.callback_query_handler(lambda c: c.data == 'wrong')
async def process_callback_button1(callback_query: CallbackQuery):
    if commhandlers.data.id == callback_query.from_user.id:
        await bot.answer_callback_query(callback_query.id)
        user_id = commhandlers.data.id
        user_name = commhandlers.data.username
        print(user_id, user_name)
        message_obj = await bot.send_message(callback_query.message.chat.id, f'Пользователь @{user_name} провалил капчу! Ответ выбран неправильно. Пользователь исключён из чата.')
        await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=message_obj.message_id - 1)
        await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=message_obj.message_id - 2)
        await ban_user(callback_query.message, user_id)
    else:
        await bot.answer_callback_query(
            callback_query.id,
            text='А это не для тебя 🤡', show_alert=True)

async def delete_msg(message, message_obj):
    await bot.edit_message_text(chat_id=message.chat.id, message_id=message_obj.message_id,
                                text="Правильно! \n \n"
                                     "Удаляю через 1.")
    time.sleep(1)
    await bot.edit_message_text(chat_id=message.chat.id, message_id=message_obj.message_id,
                                text="Правильно! \n \n"
                                     "Удаляю через 2..")
    time.sleep(2)
    await bot.edit_message_text(chat_id=message.chat.id, message_id=message_obj.message_id,
                                text="Правильно! \n \n"
                                     "Удаляю через 3...")
    time.sleep(3)
    await bot.delete_message(chat_id=message.chat.id, message_id=message_obj.message_id-1)
    await bot.delete_message(chat_id=message.chat.id, message_id=message_obj.message_id-2)
    await bot.edit_message_text(chat_id=message.chat.id, message_id=message_obj.message_id,
                                text="Пользователь прошёл капчу!")

async def ban_user(message, target_user_id):
    if target_user_id != message.chat.id:
        bot.kick_chat_member(
            chat_id=message.chat.id,
            user_id=target_user_id,
            until_date=int(time.time() + 1))
            #until_date=int(time.time() + 86400))      Нужно это, а не верхнее. Это - забанить на сутки

    else:
        await bot.send_message(message.chat.id, 'Не будем тебя банить, хехе')
