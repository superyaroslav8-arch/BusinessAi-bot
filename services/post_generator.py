from aiogram import Bot

async def generate_post(topic: str) -> str:
    """Генерация готового поста по теме"""
    return (
        f"🔥 <b>{topic.strip().capitalize()}</b>\n\n"
        f"Сегодня разбираем важную тему для бизнеса.\n\n"
        f"✅ Что важно знать\n"
        f"✅ Как применить на практике\n"
        f"✅ Какие результаты можно получить\n\n"
        f"Пишите в Direct или оставляйте заявку в боте — поможем внедрить.\n\n"
        f"#бизнес #ai #автоматизация"
    )

async def publish_post(bot: Bot, text: str, target) -> bool:
    """Публикация поста в канал или личку"""
    try:
        if isinstance(target, str) and target.startswith("@"):
            await bot.send_message(chat_id=target, text=text)
        else:
            await bot.send_message(chat_id=int(target), text=text)
        return True
    except Exception as e:
        print(f"Ошибка публикации: {e}")
        return False
