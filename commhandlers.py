import random
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import CallbackQuery
from asyncpg import Connection, Record
from asyncpg.exceptions import UniqueViolationError
from keyboards import captcha

from loader import bot, dp, db

class reg(StatesGroup):
    pic = State()
    answer = State()
    end = State()
    pic_id = ""
    ans = 0

class DBCommands:
    pool: Connection = db
    ADD_NEW_USER_REFERRAL = "INSERT INTO users(chat_id, username, full_name, referral) " \
                            "VALUES ($1, $2, $3, $4) RETURNING id"
    ADD_NEW_USER = "INSERT INTO users(chat_id, username, full_name) VALUES ($1, $2, $3) RETURNING id"
    COUNT_USERS = "SELECT COUNT(*) FROM users"
    GET_ID = "SELECT id FROM users WHERE chat_id = $1"
    CHECK_REFERRALS = "SELECT chat id FROM users WHERE referrals=" \
                      "(SELECT id FROM users WHERE chat id = $1)"
    CHECK_BALANCE = "SELECT balance FROM users WHERE chat_id = $1"
    ADD_MONEY = "UPDATE users SET balance = balance + $1 WHERE chat_id = $2"
    GET_IMAGE = "SELECT picture FROM captcha ORDER BY RANDOM() LIMIT 1"
    GET_ANS = "SELECT answer FROM captcha WHERE picture = $1"
    GET_WRONG = "SELECT wrong_answers FROM captcha WHERE picture = $1"
    ADD_NEW_IMG = "INSERT INTO captcha(picture, answer) VALUES ($1, $2)"

    async def add_new_user(self):
        user = types.User.get_current()

        chat_id = user.id
        username = user.username
        full_name = user.full_name
        args = chat_id, username, full_name
        command = self.ADD_NEW_USER

        try:
            record_id = await self.pool.fetchval(command, *args)
            return record_id
        except UniqueViolationError:
            pass

    async def count_users(self):
        record: Record = await self.pool.fetchval(self.COUNT_USERS)
        return record

    async def get_id(self):
        command = self.GET_ID
        user_id = types.User.get_current().id
        return await self.pool.fetchval(command, user_id)

    async def check_referrals(self):
        command = self.CHECK_REFERRALS
        user_id = types.User.get_current().id
        rows = await self.pool.fetch(command, user_id)
        text = ""
        for num, row in enumerate(rows):
            chat = await bot.get_chat(row["chat_id"])
            user_link = chat.get_mention(as_html=True)
            text += str(num+1) + ". " + user_link
        return text

    async def check_balance(self):
        command = self.CHECK_BALANCE
        user_id = types.User.get_current()
        return await self.pool.fetchval(command, user_id)

    async def add_money(self, money):
        command = self.ADD_MONEY
        user_id = types.User.get_current()
        return await self.pool.fetchval(command, money, user_id)

    async def get_image(self):
        command = self.GET_IMAGE
        return await self.pool.fetchval(command)

    async def get_ans(self, pic):
        command = self.GET_ANS
        return await self.pool.fetchval(command, pic)

    async def get_wrong(self, pic):
        command = self.GET_WRONG
        return await self.pool.fetchval(command, pic)

    async def add_new_img(self, img_id, img_answer):
        command = self.ADD_NEW_IMG
        user = types.User.get_current()
        chat_id = user.id
        args = img_id, img_answer

        try:
            record = await self.pool.fetchval(command, *args)
            await bot.send_message(chat_id, "Записано!")
        except UniqueViolationError:
            pass

database = DBCommands()

@dp.message_handler(commands=["start"])
async def register_user(message: types.Message):
    chat_id = message.chat.id
    count_users = await database.count_users()
    img = await database.get_image()
    text = ""
    bot_username = (await bot.get_me()).username
    text += f"""
    Представим, что это капча:
    """
    #answer = await database.get_ans(img)   # !!!!!! вне теста нам нужно вот это а сердце не нужно!!!!!!
    answer = '❤'
    wrong = await database.get_wrong(img)
    values = wrong.split(', ')
    values .insert(0, answer)

    await bot.send_message(chat_id, text)
    await dp.bot.send_photo(chat_id, img)
    random.shuffle(values)
    await message.answer("Что на картинке?",
                         reply_markup=captcha.create_keyboard(values, answer))

@dp.message_handler(commands="del")
async def delete(message: types.Message):
    await bot.delete_message(message.chat.id, message.message_id-1)

@dp.message_handler(commands="reg", state="*")
async def pic_step(message: types.Message, state: FSMContext):
    await message.answer(text='Давай фотку')
    await reg.pic.set()

@dp.message_handler(state=reg.pic, content_types=['photo'])
async def ans_step(message: types.Message, state: FSMContext):
    chat_id = message.from_user.id
    await bot.send_message(chat_id, "Получена фоточка!")
    document_id = message.photo[0].file_id
    file_info = await bot.get_file(document_id)
    print(f'file_id: {file_info.file_id}')
    print(f'file_path: {file_info.file_path}')
    print(f'file_size: {file_info.file_size}')
    print(f'file_unique_id: {file_info.file_unique_id}')
    await state.update_data(pic_id=file_info.file_id)
    await message.answer(text='Давай ответ')
    await reg.answer.set()


@dp.message_handler(state=reg.answer, content_types=types.ContentTypes.TEXT)
async def end_step(message: types.Message, state: FSMContext):
    if not(map(str.isdigit, message.text)):
        await message.reply("Цифру, пожалуйста")
        return
    await message.answer(text='Спасибо!')
    await state.update_data(ans=message.text.title())
    await reg.end.set()
    user_data = await state.get_data()
    await database.add_new_img(user_data.get('pic_id'), user_data.get('ans'))
    await state.finish()

"""------------------------------------------------------------------------------------------------------------------"""

@dp.callback_query_handler(lambda c: c.data == 'answer')
async def process_callback_button1(callback_query: CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.message.chat.id, 'Правильно!')
    #await bot.delete_message(types.Message.chat.id, types.Message.message_id)

@dp.callback_query_handler(lambda c: c.data == 'wrong')
async def process_callback_button1(callback_query: CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.message.chat.id, 'Неправильно!')
