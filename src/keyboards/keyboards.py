from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from services.price import MATERIAL_PRICES

MATERIALS = [
    f"Без утепления (однослойная штора): {MATERIAL_PRICES[0]} ₽",
    f"Стёганый синтепон: {MATERIAL_PRICES[1]} ₽",
    f"Синтепон + стёганый синтепон: {MATERIAL_PRICES[2]} ₽",
    f"Синтепон + брезент: {MATERIAL_PRICES[3]} ₽",
]


def materials_kb():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=m)] for m in MATERIALS],
        resize_keyboard=True
    )


def new_calc_kb():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Рассчитать новую штору")]],
        resize_keyboard=True
    )
