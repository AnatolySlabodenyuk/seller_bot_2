from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup

from lexicon.buttons_enum import ButtonsEnum
from lexicon.lexicon_ru import LEXICON_RU
from keyboards.keyboards import materials_kb, MATERIALS, new_calc_kb
from services.calc import calc
from config_data.config import SELLER_LOGIN

router = Router()


class CurtainForm(StatesGroup):
    material = State()
    height = State()
    width = State()
    call_with_seller = State()


@router.message(CommandStart())
async def start(msg: Message, state: FSMContext):
    await state.set_state(CurtainForm.material)
    await msg.answer(LEXICON_RU['start'], reply_markup=materials_kb())


@router.message(CurtainForm.material)
async def get_material(msg: Message, state: FSMContext):
    if msg.text not in MATERIALS:
        await msg.answer(LEXICON_RU['material_error'])
        return
    await state.update_data(material=msg.text)
    await state.set_state(CurtainForm.height)
    await msg.answer(LEXICON_RU['ask_height'], reply_markup=ReplyKeyboardRemove())


@router.message(CurtainForm.height)
async def get_height(msg: Message, state: FSMContext):
    try:
        height = float(msg.text.replace(",", "."))
    except ValueError:
        await msg.answer(LEXICON_RU['number_error'])
        return
    await state.update_data(height=height)
    await state.set_state(CurtainForm.width)
    await msg.answer(LEXICON_RU['ask_width'])


@router.message(CurtainForm.width)
async def get_width(msg: Message, state: FSMContext):
    try:
        width = float(msg.text.replace(",", "."))
    except ValueError:
        await msg.answer(LEXICON_RU['number_error'])
        return
    await state.update_data(width=width)
    data = await state.get_data()
    try:
        res = calc(data["width"], data["height"], data["material"])
        # Сохраняем данные для использования в кнопке "Написать продавцу"
        await state.update_data(
            calculated_material=res['material'],
            calculated_height=res['height'],
            calculated_width=res['width'],
            calculated_total=res['total']
        )

        await state.set_state(CurtainForm.call_with_seller)

        await msg.answer(
            LEXICON_RU['result'].format(
                material=res['material'],
                height=res['height'],
                width=res['width'],
                stripes=res['stripes'],
                width_with_allowance=res['width_with_allowance'],
                area=res['area'],
                total=res['total']
            ),
            reply_markup=new_calc_kb()
        )
    except ValueError as e:
        await msg.answer(f"Ошибка: {e}. Максимальная ширина: 7.9 м", reply_markup=ReplyKeyboardRemove())
        await state.clear()


@router.message(F.text == ButtonsEnum.CALL_TO_SELLER_BUTTON.value)
async def contact_seller(msg: Message, state: FSMContext):
    # Получаем данные последнего расчета из состояния
    data = await state.get_data()

    if not data.get('calculated_material'):
        await msg.answer("Сначала рассчитайте стоимость шторы, чтобы написать продавцу с параметрами.")
        return

    # Создаем inline кнопку для перехода к продавцу
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=ButtonsEnum.CALL_TO_SELLER_BUTTON.value, url=f"https://t.me/{SELLER_LOGIN}")]
        ]
    )

    await msg.answer(
        f"Скопируйте этот текст 👇\n\n",
    )
    await msg.answer(
        LEXICON_RU['message_text_to_seller'].format(
            calculated_material=data['calculated_material'],
            calculated_height=data['calculated_height'],
            calculated_width=data['calculated_width'],
            calculated_total=data['calculated_total']
        )
    )
    await msg.answer(
        f"🔘 Нажмите кнопку ниже, чтобы перейти в чат с продавцом, и вставьте скопированный текст:",
        reply_markup=keyboard
    )


@router.message(F.text == ButtonsEnum.RESTART_BUTTON.value)
async def new_calc(msg: Message, state: FSMContext):
    await state.clear()
    await state.set_state(CurtainForm.material)
    await msg.answer(LEXICON_RU['start'], reply_markup=materials_kb())
