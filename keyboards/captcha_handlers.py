import asyncio
import time

from aiogram.types import CallbackQuery, Message
import commhandlers
from loader import bot, dp

@dp.callback_query_handler(lambda c: c.data == 'answer')
async def process_callback_button1(callback_query: CallbackQuery):

    await bot.answer_callback_query(callback_query.id)
    message_obj = await bot.send_message(callback_query.message.chat.id, 'Правильно!')
    if not commhandlers.success: commhandlers.success = True
    await delete_msg(callback_query.message, message_obj)


@dp.callback_query_handler(lambda c: c.data == 'wrong')
async def process_callback_button1(callback_query: CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    message_obj = await bot.send_message(callback_query.message.chat.id, 'Пользователь провалил капчу! Ответ выбран неправильно.')
    await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=message_obj.message_id - 1)
    await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=message_obj.message_id - 2)

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
