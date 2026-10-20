from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from keyboards.main_menu import main_menu_kb

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    text = (
        "<b>Business Ai</b> — ваш AI-помощник для бизнеса 24/7\n\n"
        "Я умею:\n"
        "• Автоматически отвечать клиентам\n"
        "• Проводить консультации\n"
        "• Создавать и публиковать посты\n"
        "• Собирать заявки\n\n"
        "Выберите действие в меню или просто напишите вопрос."
    )
    await message.answer(text, reply_markup=main_menu_kb())

@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(
        "<b>Команды:</b>\n"
        "/start — главное меню\n"
        "/lead — оставить заявку\n"
        "/post — создать пост\n"
        "/consult — консультация\n"
        "/stats — статистика (только админ)\n\n"
        "Или просто пишите — я отвечу автоматически."
    )
