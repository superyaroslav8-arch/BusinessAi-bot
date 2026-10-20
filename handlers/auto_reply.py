from aiogram import Router, F
from aiogram.types import Message
from services.ai_engine import generate_reply

router = Router()

# Автоответчик на любые текстовые сообщения (работает 24/7)
@router.message(F.text)
async def auto_reply_handler(message: Message):
    # Игнорируем команды (они обрабатываются раньше)
    if message.text.startswith("/"):
        return

    reply = await generate_reply(message.text, user_id=message.from_user.id)
    await message.answer(reply)
