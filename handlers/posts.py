from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from keyboards.main_menu import posts_kb
from services.post_generator import generate_post, publish_post
import os

router = Router()
CHANNEL_ID = os.getenv("CHANNEL_ID", "")

class PostStates(StatesGroup):
    waiting_topic = State()
    waiting_confirm = State()

@router.message(Command("post"))
@router.message(F.text == "Создать пост")
async def start_post(message: Message, state: FSMContext):
    await state.set_state(PostStates.waiting_topic)
    await message.answer(
        "Напишите тему или ключевые идеи для поста.\n"
        "Я сгенерирую готовый текст для публикации.",
        reply_markup=posts_kb()
    )

@router.message(PostStates.waiting_topic)
async def generate_post_handler(message: Message, state: FSMContext):
    post_text = await generate_post(message.text)
    await state.update_data(post_text=post_text)
    await state.set_state(PostStates.waiting_confirm)
    await message.answer(
        f"<b>Готовый пост:</b>\n\n{post_text}\n\n"
        "Опубликовать?", 
        reply_markup=posts_kb(confirm=True)
    )

@router.callback_query(F.data == "post_publish")
async def publish_handler(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    post_text = data.get("post_text", "")
    if not post_text:
        await callback.answer("Нет текста поста", show_alert=True)
        return

    success = await publish_post(callback.bot, post_text, CHANNEL_ID or callback.from_user.id)
    if success:
        await callback.message.edit_text("Пост успешно опубликован!")
    else:
        await callback.message.edit_text("Не удалось опубликовать. Проверьте CHANNEL_ID или права бота.")
    await state.clear()
    await callback.answer()

@router.callback_query(F.data == "post_cancel")
async def cancel_post(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text("Создание поста отменено.")
    await callback.answer()
