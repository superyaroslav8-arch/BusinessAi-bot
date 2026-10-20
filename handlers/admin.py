from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from services.leads_storage import get_all_leads
import os

router = Router()
ADMIN_IDS = [int(x.strip()) for x in os.getenv("ADMIN_IDS", "").split(",") if x.strip()]

def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS

@router.message(Command("stats"))
async def cmd_stats(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("Команда только для администратора.")
        return

    leads = get_all_leads()
    text = f"<b>Статистика Business Ai</b>\n\nВсего заявок: {len(leads)}\n\n"
    for i, lead in enumerate(leads[-10:], 1):
        text += (
            f"{i}. {lead.get('name')} — {lead.get('contact')}\n"
            f"   {lead.get('request')[:50]}...\n\n"
        )
    await message.answer(text or "Заявок пока нет.")
