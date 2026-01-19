"""
358-maktab ingliz tili Telegram bot
Main entry point
"""

import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Import handlers
from handlers.start_handler import start_router
from handlers.menu_handler import menu_router
from handlers.material_handler import material_router
from handlers.test_handler import test_router

# Import database
from utils.db import init_db

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Bot token from .env
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN topilmadi! .env faylni tekshiring.")


async def main():
    """Main function to start the bot"""
    # Initialize database
    init_db()
    logger.info("Database initialized")

    # Initialize bot and dispatcher
    bot = Bot(token=BOT_TOKEN)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    # Register routers
    dp.include_router(start_router)
    dp.include_router(menu_router)
    dp.include_router(material_router)
    dp.include_router(test_router)

    logger.info("Bot ishga tushdi...")

    # Start polling
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
