from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def main_menu_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Консультация"), KeyboardButton(text="Оставить заявку")],
            [KeyboardButton(text="Создать пост")],
        ],
        resize_keyboard=True,
        input_field_placeholder="Напишите вопрос или выберите действие"
    )

def consult_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Отмена", callback_data="consult_cancel")]
    ])

def posts_kb(confirm: bool = False) -> InlineKeyboardMarkup:
    if confirm:
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Опубликовать", callback_data="post_publish")],
            [InlineKeyboardButton(text="Отмена", callback_data="post_cancel")],
        ])
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Отмена", callback_data="post_cancel")]
    ])

def leads_kb(done: bool = False) -> InlineKeyboardMarkup:
    if done:
        return InlineKeyboardMarkup(inline_keyboard=[])
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Отмена", callback_data="lead_cancel")]
    ])
