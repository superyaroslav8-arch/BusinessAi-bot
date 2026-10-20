from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from keyboards.main_menu import consult_kb
from services.ai_engine import generate_consultation

router = Router()

class ConsultStates(StatesGroup):
    waiting_question = State()

@router.message(Command("consult"))
@router.message(F.text == "Консультация")
async def start_consult(message: Message, state: FSMContext):
    await state.set_state(ConsultStates.waiting_question)
    await message.answer(
        "Задайте любой вопрос по бизнесу, услугам, ценам или стратегии.\n"
        "Я дам развёрнутую консультацию.",
        reply_markup=consult_kb()
    )

@router.message(ConsultStates.waiting_question)
async def process_consult(message: Message, state: FSMContext):
    answer = await generate_consultation(message.text)
    await message.answer(answer)
    await state.clear()

@router.callback_query(F.data == "consult_cancel")
async def cancel_consult(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text("Консультация отменена.")
    await callback.answer()
