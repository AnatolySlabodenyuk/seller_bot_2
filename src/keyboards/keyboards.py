from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

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
            [KeyboardButton(text="💰 Рассчитать новую штору")],
            [KeyboardButton(text="📞 Написать продавцу")]
        ],
        resize_keyboard=True
    )
