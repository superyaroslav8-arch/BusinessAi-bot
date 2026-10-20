import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dotenv import load_dotenv
import os

from handlers import start, auto_reply, consultation, posts, leads, admin

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN", "8947636785:AAEHgcdIj7jsSGnipAynXbsib-ZuYn2QRTY")
ADMIN_IDS = [int(x.strip()) for x in os.getenv("ADMIN_IDS", "").split(",") if x.strip()]

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(storage=MemoryStorage())

    # Регистрация роутеров
    dp.include_router(start.router)
    dp.include_router(leads.router)
    dp.include_router(consultation.router)
    dp.include_router(posts.router)
    dp.include_router(admin.router)
    dp.include_router(auto_reply.router)  # общий автоответчик — последним

    logger.info("Business Ai бот запущен 24/7")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
