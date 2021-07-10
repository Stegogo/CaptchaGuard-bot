import logging

from aiogram.dispatcher import FSMContext

from loader import dp
from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram import types
from states.test import Test
from keyboards.inline.choice_buttons import choice


@dp.message_handler(Command("test"), state=None)
async def show_items(message: Message):
    await message.answer(text="Some text",
                         reply_markup=choice)
    await Test.Q1.set()

@dp.message_handler(state=Test.Q1)
async def answer_q1(message: types.Message, state: FSMContext):
    answer1 = message.text
    await state.update_data(answer1=answer1)
    await message.answer("Another text!")
    await Test.next()

@dp.message_handler(state=Test.Q2)
async def answer_q1(message: types.Message, state: FSMContext):
    data = await state.get_data()
    answer1 = data.get("answer1")
    answer2 = message.text

    await message.answer("Thanks")
    await state.reset_state(with_data=False)

@dp.callback_query_handler(text_contains="B")
async def calling_B(call: CallbackQuery):
    await call.answer(cache_time=60)
    callback_data = call.data
    logging.info(f"call={callback_data}")

    await call.message.answer(text="BBB!!!!!")
