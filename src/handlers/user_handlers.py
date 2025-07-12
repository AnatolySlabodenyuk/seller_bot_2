from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, ReplyKeyboardRemove
from lexicon.lexicon_ru import LEXICON_RU
from keyboards.keyboards import materials_kb, options_kb, MATERIALS, OPTIONS
from services.calc import calc

router = Router()


class CurtainForm(StatesGroup):
    material = State()
    height = State()
    width = State()
    options = State()


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
    await state.update_data(options=[])
    await state.set_state(CurtainForm.options)
    await msg.answer(LEXICON_RU['ask_options'], reply_markup=options_kb())


@router.message(CurtainForm.options)
async def get_options(msg: Message, state: FSMContext):
    data = await state.get_data()
    options = data.get("options", [])
    if msg.text == "Готово":
        try:
            res = calc(data["width"], data["height"], data["material"], options)
            opts = ", ".join(res["opts"]) if res["opts"] else "—"
            await msg.answer(
                LEXICON_RU['result'].format(
                    material=res['material'],
                    height=res['height'],
                    width=res['width'],
                    stripes=res['stripes'],
                    width_with_allowance=res['width_with_allowance'],
                    area=res['area'],
                    base_cost=res['base_cost'],
                    opts=opts,
                    total=res['total']
                ),
                reply_markup=ReplyKeyboardRemove()
            )
            await state.clear()
        except ValueError as e:
            await msg.answer(f"Ошибка: {e}. Максимальная ширина: 7.9 м", reply_markup=ReplyKeyboardRemove())
            await state.clear()
    elif msg.text in OPTIONS:
        if msg.text not in options:
            options.append(msg.text)
            await state.update_data(options=options)
        await msg.answer(LEXICON_RU['option_added'].format(option=msg.text), reply_markup=options_kb())
    else:
        await msg.answer(LEXICON_RU['option_error'])
