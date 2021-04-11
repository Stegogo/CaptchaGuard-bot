from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.inline.callback_datas import test_callback

"""choice = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardMarkup(text='A', callback_data=test_callback.new(
                item_name="AAAAAA"
            )),
            InlineKeyboardMarkup(text='B', callback_data=""),
            InlineKeyboardMarkup(text='C', callback_data="")
        ],
        [
            InlineKeyboardMarkup(text='Cancel', callback_data="cancel")
        ]
    ]
)"""

choice = InlineKeyboardMarkup(row_width=1)

testB = InlineKeyboardButton(text='B',
                             callback_data=test_callback.new(
                                 item_name="BBBBBBBB"
                             ))
choice.insert(testB)
testC = InlineKeyboardButton(text='C',
                             callback_data=test_callback.new(
                                 item_name="CCCCCCC"
                             ))
choice.insert(testC)
cancel_button = InlineKeyboardButton(text="Cancel", callback_data="cancel")
choice.insert(cancel_button)