from loader import dp
from aiogram.dispatcher.filters import Command
from aiogram.types import Message
from keyboards.inline.choice_buttons import choice

@dp.message_handler(Command("test"))
async def show_items(message: Message):
    await message.answer(text="Some text",
                         reply_markup=choice)
