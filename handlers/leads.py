from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from keyboards.main_menu import leads_kb
from services.leads_storage import save_lead, get_all_leads
import os

router = Router()
ADMIN_IDS = [int(x.strip()) for x in os.getenv("ADMIN_IDS", "").split(",") if x.strip()]

class LeadStates(StatesGroup):
    waiting_name = State()
    waiting_contact = State()
    waiting_request = State()

@router.message(Command("lead"))
@router.message(F.text == "Оставить заявку")
async def start_lead(message: Message, state: FSMContext):
    await state.set_state(LeadStates.waiting_name)
    await message.answer(
        "Давайте оформим заявку.\n\nКак вас зовут?",
        reply_markup=leads_kb()
    )

@router.message(LeadStates.waiting_name)
async def lead_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(LeadStates.waiting_contact)
    await message.answer("Укажите телефон или @username для связи:")

@router.message(LeadStates.waiting_contact)
async def lead_contact(message: Message, state: FSMContext):
    await state.update_data(contact=message.text)
    await state.set_state(LeadStates.waiting_request)
    await message.answer("Кратко опишите, что вам нужно:")

@router.message(LeadStates.waiting_request)
async def lead_request(message: Message, state: FSMContext):
    data = await state.get_data()
    lead = {
        "name": data.get("name"),
        "contact": data.get("contact"),
        "request": message.text,
        "user_id": message.from_user.id,
        "username": message.from_user.username or "",
    }
    save_lead(lead)

    # Уведомление админам
    notify_text = (
        f"<b>Новая заявка!</b>\n\n"
        f"Имя: {lead['name']}\n"
        f"Контакт: {lead['contact']}\n"
        f"Запрос: {lead['request']}\n"
        f"От: @{lead['username']} (id: {lead['user_id']})"
    )
    for admin_id in ADMIN_IDS:
        try:
            await message.bot.send_message(admin_id, notify_text)
        except Exception:
            pass

    await message.answer(
        "Спасибо! Заявка принята. Мы свяжемся с вами в ближайшее время.",
        reply_markup=leads_kb(done=True)
    )
    await state.clear()

@router.callback_query(F.data == "lead_cancel")
async def cancel_lead(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text("Заявка отменена.")
    await callback.answer()
