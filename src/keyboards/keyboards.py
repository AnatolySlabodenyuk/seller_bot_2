from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from lexicon.buttons_enum import ButtonsEnum
from services.price import MATERIAL_PRICES

MATERIALS = [
    "Без утепления (однослойная штора)",
    "Стёганый синтепон",
    "Синтепон + стёганый синтепон",
    "Синтепон + брезент",
]


def materials_kb():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=m)] for m in MATERIALS],
        resize_keyboard=True
    )


def new_calc_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=ButtonsEnum.RESTART_BUTTON.value)],
            [KeyboardButton(text=ButtonsEnum.CALL_TO_SELLER_BUTTON.value)]
        ],
        resize_keyboard=True
    )
