import time

from aiogram.types import CallbackQuery
import commhandlers
from loader import bot, dp, _

@dp.callback_query_handler(lambda c: c.data == 'answer')
async def process_callback_button1(callback_query: CallbackQuery):
    if commhandlers.data.id == callback_query.from_user.id:
        await bot.answer_callback_query(callback_query.id)
        if not commhandlers.success: commhandlers.success = True
        pic_id = commhandlers.pic_msg
        await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=pic_id - 2)
        await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=pic_id - 1)
        await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=pic_id)
        await bot.send_message(callback_query.message.chat.id, 'Правильно!')

        greet_text = await commhandlers.database.get_greeting(callback_query.message.chat.id)
        if greet_text != " ":
            text = str(greet_text)
            if "$user" in text:
                text = text.replace("$user", f"@{callback_query.from_user.username}")
            await bot.send_message(callback_query.message.chat.id, text)
        else:
            pass
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
        pic_id = commhandlers.pic_msg
        await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=pic_id - 2)
        await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=pic_id - 1)
        await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=pic_id)
        await bot.send_message(callback_query.message.chat.id, f'Пользователь @{user_name} провалил капчу! Ответ выбран неправильно. Пользователь исключён из чата.')
        await ban_user(callback_query.message, user_id)
    else:
        await bot.answer_callback_query(
            callback_query.id,
            text='А это не для тебя 🤡', show_alert=True)

async def ban_user(message, target_user_id):
    if target_user_id != message.chat.id:
        await bot.kick_chat_member(
            chat_id=message.chat.id,
            user_id=target_user_id,
            until_date=int(time.time() + 12))
            #until_date=int(time.time() + 86400))      Нужно это, а не верхнее. Это - забанить на сутки

    else:
        await bot.send_message(message.chat.id, 'Не будем тебя банить, хехе')
