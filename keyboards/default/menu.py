from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="A"),
        ],
        [
            KeyboardButton(text='B'),
            KeyboardButton(text='C')
        ],
    ],
    resize_keyboard=True
)
