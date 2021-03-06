import asyncio
import random
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from asyncpg import Connection, Record
from asyncpg.exceptions import UniqueViolationError
from babel import Locale
from data import config
from keyboards import captcha, captcha_handlers
import handlers.bot_options.options_handlers
import psycopg2
import psycopg2.extras

from loader import bot, dp, db, _
import os

success = False
data = None
pic_msg = None

class Reg(StatesGroup):
    pic = State()
    answer = State()
    end = State()
    pic_id = ""
    ans = ""
    wrong_ans = ""

class DBCommands:
    pool: Connection = db
    cursor = db.cursor()
    cursor.execute("SELECT * FROM user")
    for buff in cursor:
        row = {}
        c = 0
        for col in cursor.description:
            row.update({str(col[0]): buff[c]})
            c += 1

    GET_ID = "SELECT id FROM users WHERE chat_id = %s"
    GET_IMAGE = "SELECT picture FROM captcha ORDER BY RANDOM() LIMIT 1"
    GET_ANS = "SELECT answer FROM captcha WHERE picture = %s"
    GET_WRONG = "SELECT wrong_answers FROM captcha WHERE picture = %s"
    ADD_NEW_IMG = "INSERT INTO captcha(picture, answer, wrong_answers) VALUES (%s, %s, %s)"

    ADD_NEW_CHAT_ID = "INSERT INTO users(chat_id, lang, greet, protect) VALUES (%s, %s, %s, %s)"
    SET_LANG = "UPDATE users SET lang=%s WHERE chat_id = %s"
    SET_NEW_GREETING = "UPDATE users SET greet=%s WHERE chat_id = %s"
    SET_PROTECTION = "UPDATE users SET protect=%s WHERE chat_id = %s"
    GET_LANG = "SELECT lang FROM users WHERE chat_id = %s"
    GET_GREET = "SELECT greet FROM users WHERE chat_id = %s"
    GET_PROTECT = "SELECT protect FROM users WHERE chat_id = %s"

    async def get_id(self):
        command = self.GET_ID
        user_id = types.User.get_current().id
        self.cursor.execute(command, (user_id,))
        x = self.cursor.fetchone()
        return x[0]

    async def get_image(self):
        command = self.GET_IMAGE
        self.cursor.execute(command)
        x = self.cursor.fetchone()
        print(x)
        return x[0]

    async def get_ans(self, pic):
        command = self.GET_ANS
        self.cursor.execute(command, (pic,))
        x = self.cursor.fetchone()
        return x[0]

    async def get_wrong(self, pic):
        command = self.GET_WRONG
        self.cursor.execute(command, (pic,))
        x = self.cursor.fetchone()
        return x[0]

    async def add_new_img(self, img_id, img_answer, wrong_ans):
        command = self.ADD_NEW_IMG
        user = types.User.get_current()
        chat_id = user.id
        args = (img_id, img_answer, wrong_ans)

        try:
            self.cursor.execute(command, args)
            await bot.send_message(chat_id, "????????????????!")
        except UniqueViolationError:
            await bot.send_message(chat_id, "????.")

    async def add_new_chat_id(self, chat_id, lang, greet, protect, message):
        command = self.ADD_NEW_CHAT_ID
        args = (chat_id, lang, greet, protect)
        await handlers.bot_options.options_handlers.send_about(message)
        try:
            self.cursor.execute(command, args)
        except UniqueViolationError:
            pass

    async def set_new_greeting(self, chat_id, text):
        command = self.SET_NEW_GREETING
        ch_id = str(chat_id)
        return self.cursor.execute(command, (text, ch_id))

    async def set_new_lang(self, chat_id, language):
        command = self.SET_LANG
        ch_id = str(chat_id)
        return self.cursor.execute(command, (language, ch_id))

    async def set_new_protect(self, chat_id, protect_mode):
        command = self.SET_PROTECTION
        ch_id = str(chat_id)
        return self.cursor.execute(command, (protect_mode, ch_id))

    async def get_greeting(self, chat_id):
        command = self.GET_GREET
        ch_id = str(chat_id)
        self.cursor.execute(command, (ch_id,))
        x = self.cursor.fetchone()
        return x[0]

    async def get_lang(self, chat_id):
        command = self.GET_LANG
        ch_id = str(chat_id)
        self.cursor.execute(command, (ch_id,))
        x = self.cursor.fetchone()
        return x[0]

    async def get_protect(self, chat_id):
        command = self.GET_PROTECT
        ch_id = str(chat_id)
        self.cursor.execute(command, (ch_id,))
        x = self.cursor.fetchone()
        return x[0]


database = DBCommands()

async def register_user(message: types.Message, target_user_data):
    global success, pic_msg
    chat_id = message.chat.id
    mode = await database.get_protect(chat_id)
    if mode == 'True':
        if success: success = False
        img = await database.get_image()
        text = ""
        try:
            text += _(f"""
            ????????????, $user! ????????????, ?????? ???? ???? ??????, ?? ?????? ?????????? ???? ???????????? ?? ???????????????? ????????. ?? ???????? ???????? 60 ????????????!
            """).replace('$user!', f'@{target_user_data.username}!')
        except:
            text += _(f"""
            ????????????! ????????????, ?????? ???? ???? ??????, ?? ?????? ?????????? ???? ???????????? ?? ???????????????? ????????. ?? ???????? ???????? 60 ????????????!
            """)
        answer = await database.get_ans(img)
        wrong = await database.get_wrong(img)
        values = wrong.split(', ')
        values .insert(0, answer)

        await bot.send_message(chat_id, text)
        await dp.bot.send_photo(chat_id, img)
        random.shuffle(values)
        msg1 = await message.answer(_("????????????? ???? ???????????????????? ?????????????"), reply_markup=captcha.create_keyboard(values, answer))
        pic_msg = int(msg1)
        if not success: asyncio.ensure_future(timer(message, msg1))
    else:
        pass

async def timer(message: types.Message, msg1):
    my_task = None
    global success
    while not success:
        await asyncio.sleep(0)
        if not success and my_task is None:
            my_task = asyncio.ensure_future(failed_captcha(message, msg1))
        elif success and my_task:
            if not my_task.cancelled():
                my_task.cancel()
                success = True

async def failed_captcha(message: types.Message, msg1):
    await asyncio.sleep(60)
    global data
    await bot.edit_message_text(chat_id=message.chat.id, message_id=msg1.message_id,
                                text=(_(f"???????????????????????? ???????????????? ??????????! ?????????? ???? ?????? ????????????. ???????????????????????? ???????????????? ???? ????????.")))
    await bot.delete_message(chat_id=message.chat.id, message_id=msg1.message_id-1)
    await captcha_handlers.ban_user(message, data.id)


@dp.message_handler(content_types=["new_chat_members"])
async def handler_new_member(message: types.Message):
    me = await bot.get_me()
    if message.new_chat_members[0].id != me.id:
        global data
        target_user_data = message.new_chat_members[0]
        data = target_user_data
        if not message.new_chat_members[0].is_bot:
            if data is None:
                pass
            else:
                await register_user(message, target_user_data)
    else:
        await database.add_new_chat_id(message.chat.id, "en", " ", "True", message)     # Default options

@dp.message_handler(commands="start")
async def ans_step(message: types.Message, state: FSMContext):
    text = _(f"""
????????????! ???? ?? - CaptchaGuard!
?? ??????, ?????????????? ???????????????? ???????????? ?????????????????? ???????? ???? ??????????????????????????-??????????.\n
?????????? ?? ?????????? ???????????????? - ???????????????? ???????? ?? ?????? ?? ???????????????? ??????????????????????????????.\n
CaptchaGuard - ?????? ?? ???????????????? ??????????!
https://github.com/Stegogo/CaptchaGuard-bot\n
????????????????????, ???????????????????? ???????????????????????? ???? ?????????? ??????5168755455346094\n
?????????????????? ??????????????:
/menu: ?????????????? ???????? ??????
/contact: ???????????????? ???????????????????????? ??????
    """)
    await message.answer(text=text, disable_web_page_preview=True)

# Adding new captcha to the database
@dp.message_handler(commands="reg", state="*")  # Command available only for bot admin (id stated in .env)
async def pic_step(message: types.Message):
    chat_id = message.chat.id
    if chat_id == int(config.ADMINS):
        await message.answer('?????????????? ???????????????? ?? ????????????')
        await Reg.pic.set()
    else:
        pass

@dp.message_handler(state=Reg.pic, content_types=['photo'])
async def ans_step(message: types.Message, state: FSMContext):
    chat_id = message.from_user.id
    await bot.send_message(chat_id, "????????!")
    document_id = message.photo[0].file_id
    file_info = await bot.get_file(document_id)
    print(f'file_id: {file_info.file_id}')
    print(f'file_path: {file_info.file_path}')
    print(f'file_size: {file_info.file_size}')
    print(f'file_unique_id: {file_info.file_unique_id}')
    await state.update_data(pic_id=file_info.file_id)
    await message.answer(text='?????????? ??????????')
    await Reg.answer.set()

@dp.message_handler(state=Reg.answer, content_types=types.ContentTypes.TEXT)
async def end_step(message: types.Message, state: FSMContext):
    await state.update_data(ans=message.text.title())
    await message.answer(text='???????????? ?????????? ???????? ???????????????????????? ?????????????? ?? ???????????? ?????????? ??????????????.'
                              '????????????????: "1, 2, 3, 4, 5"')
    await Reg.end.set()

@dp.message_handler(state=Reg.end, content_types=types.ContentTypes.TEXT)
async def end_step(message: types.Message, state: FSMContext):
    await state.update_data(wrong_ans=message.text.title())
    await message.answer(text='??????????????!')
    user_data = await state.get_data()
    await database.add_new_img(user_data.get('pic_id'), user_data.get('ans'), user_data.get('wrong_ans'))
    await state.finish()
