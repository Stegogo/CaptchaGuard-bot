from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from random import shuffle

def create_keyboard(values, answer):
    inline_kb_full = InlineKeyboardMarkup(row_width=3)
    btn_1 = InlineKeyboardButton(values[0], callback_data='wrong')
    btn_2 = InlineKeyboardButton(values[1], callback_data='wrong')
    btn_3 = InlineKeyboardButton(values[2], callback_data='wrong')
    btn_4 = InlineKeyboardButton(values[3], callback_data='wrong')
    btn_5 = InlineKeyboardButton(values[4], callback_data='wrong')
    btn_6 = InlineKeyboardButton(values[5], callback_data='wrong')
    inline_kb_full.row(btn_1, btn_2, btn_3)
    inline_kb_full.row(btn_4, btn_5, btn_6)
    for x in (btn_1, btn_2, btn_3, btn_4, btn_5, btn_6):
        if x.text == answer:
            x.callback_data = 'answer'
    return inline_kb_full
