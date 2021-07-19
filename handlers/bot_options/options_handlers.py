import asyncio
import random
from aiogram import types
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from asyncpg import Connection, Record
import commhandlers
import gettext

from data import config
from loader import bot, dp, db, _

lang = None
greet = None
protect = True
non_admin_text = _("Ты не админ и не можешь настраивать меня!")

class TechSupport(StatesGroup):
    send_msg = State()
    chat_id = 0
class SupportReply(StatesGroup):
    send_msg = State()
class ReplyTo:
    msg_id = 0
    chat_id = 0

@dp.message_handler(commands="menu")
async def send_menu(message: types.Message):
    text = _(f"""
Привет! 👋 Я - CaptchaGuard, защищаю ваш чат от пользователей-ботов.\n
Вы вызвали моё меню настроек.
Пользоваться им могут только администраторы чата.\n
Доступные команды:
/set_language: Сменить язык 🌍
/set_greeting: Сменить приветствие ⭐️
/disable_captcha: Отключить капчу 🔓
/enable_captcha: Включить капчу 🔒
/contact: Написать разработчику ⚙""")
    await message.answer(text=text)

@dp.message_handler(commands="about")
async def send_about(message: types.Message):
    text = _(f"""
Привет! 👋 Я - CaptchaGuard!
Я бот, который защищает капчей публичные чаты от пользователей-ботов.\n
Как это работает:
Когда к чату присоединяется новый участник, я даю ему простую задачу, чтобы проверить, бот он или человек.
Тот кто не справился с задачей, исключается из чата!\n
CaptchaGuard - <a href="https://github.com/Stegogo/CaptchaGuard-bot">бот с открытым кодом</a>!
Пожалуйста, поддержите разработчика на карту ❤️5168755455346094 (MasterCard)\n
Доступные команды:
/menu: Главное меню ✏️
/contact: Написать разработчику ⚙️
/set_language: Сменить язык 🌍
""")
    await message.answer(text=text, disable_web_page_preview=True)

@dp.message_handler(commands="contact")
async def send_contact(message: types.Message):
    if message.chat.id != message.from_user.id:
        text = _(f"""
Чтобы написать разработчику, перейди в личные сообщения с ботом:\n
⚙️https://t.me/captchaguardbot?start=techsupport🔧\n
В личных сообщениях с ботом нажми команду contact!
Спасибо заранее! Ты получишь ответ в течение 24 часов.
""")
        await message.answer(text=text)
    else:
        await send_support(message)

@dp.message_handler(commands="techsupport", state="*")
async def send_support(message: types.Message):
    text = _(f"""
То, что ты сейчас напишешь, будет переслано разработчику!
Постарайся уместить то, что хочешь сказать, в одном сообщении ❤️\n
Чтобы отменить команду - нажми /cancel
""")
    await message.answer(text=text)
    await TechSupport.send_msg.set()

@dp.message_handler(commands="cancel", state=TechSupport.send_msg)
async def forward_cancel(message: types.Message, state: FSMContext):
    await message.answer("✅")
    await state.finish()

@dp.message_handler(state=TechSupport.send_msg, content_types=types.ContentTypes.TEXT)
async def forward_to_support(message: types.Message, state: FSMContext):
    msg = message.message_id
    await dp.bot.forward_message(int(config.ADMINS), message.chat.id, msg)
    await message.answer(_("Сообщение отправлено. Спасибо!"))
    await state.finish()

@dp.message_handler(commands="reply", state="*")
async def reply_to_user(message: types.Message):
    if message.chat.id == int(config.ADMINS):
        await message.answer("Можешь отвечать!")
        await SupportReply.send_msg.set()
    else:
        pass
@dp.message_handler(state=SupportReply.send_msg, content_types=types.ContentTypes.TEXT)
async def end_step(message: types.Message, state: FSMContext):
    msg = message.text
    await bot.send_message(message.reply_to_message.forward_from.id, msg)
    await message.answer("Ответ отправлен!")
    await state.finish()

@dp.message_handler(commands="set_greeting")
async def set_greet_1(message: types.Message):
    tmp = await bot.get_chat_administrators(message.chat.id)
    admins = [x.user.id for x in tmp]
    if message.from_user.id in admins:
        text = _(f"""
Вы можете настроить сообщение, которое будет приветствовать новых участников чата после того, как они прошли капчу.
Например, вы можете оставить ссылку на правила вашего чата или на другие важные материалы.\n
Пожалуйста, введите новое сообщение приветствия после команды, вот так:
/set_new_greeting Привет, $user, мы рады тебя видеть!\n
Вы также можете отключить приветствие:
/set_new_greeting -""")
        await message.answer(text=text)
    else:
        await message.answer(_(non_admin_text))

@dp.message_handler(commands=['set_new_greeting'])
async def set_greet_2(message: types.Message):
    tmp = await bot.get_chat_administrators(message.chat.id)
    admins = [x.user.id for x in tmp]
    if message.from_user.id in admins:
        arguments = message.get_args()
        if arguments == '-':
            await commhandlers.database.set_new_greeting(message.chat.id, " ")
        else:
            await commhandlers.database.set_new_greeting(message.chat.id, arguments)
        await message.answer(_("Сообщение приветствия изменено!"))
    else:
        await message.answer(_(non_admin_text))

@dp.message_handler(commands=['disable_captcha'])
async def set_captcha_1(message: types.Message):
    tmp = await bot.get_chat_administrators(message.chat.id)
    admins = [x.user.id for x in tmp]
    if message.from_user.id in admins:
        mode = await commhandlers.database.get_protect(message.chat.id)
        if mode == 'True':
            await commhandlers.database.set_new_protect(message.chat.id, "False")
            await message.answer(_("Капча отключена! 🔓 Если хотите вернуть её обратно, введите /enable_captcha"))
        else:
            await message.answer(_("Капча уже отключена! 🔓"))
    else:
        await message.answer(_(non_admin_text))
@dp.message_handler(commands=['enable_captcha'])
async def set_captcha_2(message: types.Message):
    tmp = await bot.get_chat_administrators(message.chat.id)
    admins = [x.user.id for x in tmp]
    if message.from_user.id in admins:
        mode = await commhandlers.database.get_protect(message.chat.id)
        if mode == 'False':
            await commhandlers.database.set_new_protect(message.chat.id, "True")
            await message.answer(_("Капча включена! 🔒 Если хотите выключить её, введите /disable_captcha"))
        else:
            await message.answer(_("Капча уже включена! 🔒"))
    else:
        await message.answer(_(non_admin_text))
@dp.message_handler(commands=['set_language'])
async def set_language(message: types.Message):
    tmp = await bot.get_chat_administrators(message.chat.id)
    admins = [x.user.id for x in tmp]
    if message.from_user.id in admins:
        languages_markup = InlineKeyboardMarkup(
            inline_keyboard=
            [
                [
                    InlineKeyboardButton(text="English 🇺🇸", callback_data="lang_en"),
                ],
                [
                    InlineKeyboardButton(text="Україньска 🇺🇦", callback_data="lang_uk"),
                    InlineKeyboardButton(text="Русский 🇷🇺", callback_data="lang_ru")
                ]
            ]
        )
        msg = await message.answer(_("Выберите язык:"), reply_markup=languages_markup)
    else:
        await message.answer(_(non_admin_text))

@dp.callback_query_handler(text_contains="lang")
async def change_language(call: CallbackQuery):
    language = call.data[-2:]
    await commhandlers.database.set_new_lang(call.message.chat.id, language)
    await call.message.edit_reply_markup()
    await call.message.edit_text("✅")

