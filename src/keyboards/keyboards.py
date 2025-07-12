from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

MATERIALS = [
    "Без утепления (однослойная штора)",
    "Стёганый синтепон",
    "Синтепон + стёганый синтепон",
    "Синтепон + брезент",
]

OPTIONS = ["Молния по центру", "Люверсы"]


def materials_kb():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=m)] for m in MATERIALS],
        resize_keyboard=True
    )


def options_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=o) for o in OPTIONS],
            [KeyboardButton(text="Готово")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
