"""
Admin notification utilities
"""

import os
from aiogram import Bot
from typing import Optional, List
import logging

logger = logging.getLogger(__name__)


def get_admin_ids() -> List[int]:
    """Get admin IDs from environment variable"""
    admin_ids_str = os.getenv("ADMIN_IDS", "")
    if not admin_ids_str:
        return []
    try:
        return [int(id.strip()) for id in admin_ids_str.split(",") if id.strip()]
    except ValueError:
        logger.error("Invalid ADMIN_IDS format in environment")
        return []


async def notify_admin_new_user(
    bot: Bot,
    telegram_id: int,
    username: Optional[str],
    phone: str,
    full_name: str
):
    """Send notification to admins about new registered user"""
    try:
        message = f"""
🆕 <b>Yangi foydalanuvchi ro'yxatdan o'tdi!</b>

👤 <b>Ism va Familiya:</b> {full_name}
📱 <b>Telefon raqami:</b> {phone}
🆔 <b>Telegram ID:</b> {telegram_id}
📝 <b>Username:</b> @{username if username else 'yo\'q'}

📅 <b>Vaqt:</b> Hozir
"""
        admin_ids = get_admin_ids()
        for admin_id in admin_ids:
            try:
                await bot.send_message(
                    chat_id=admin_id,
                    text=message,
                    parse_mode="HTML"
                )
            except Exception as e:
                logger.error(f"Failed to notify admin {admin_id}: {e}")
        logger.info(f"Admins notified about new user: {telegram_id}")
    except Exception as e:
        logger.error(f"Failed to notify admins: {e}")


async def notify_admin_test_completed(
    bot: Bot,
    telegram_id: int,
    full_name: str,
    test_name: str,
    score: float,
    correct: int,
    total: int
):
    """Send notification to admins about completed test"""
    try:
        emoji = "🏆" if score >= 80 else "📊"
        message = f"""
{emoji} <b>Test yakunlandi!</b>

👤 <b>O'quvchi:</b> {full_name}
🆔 <b>Telegram ID:</b> {telegram_id}
📝 <b>Test:</b> {test_name}
✅ <b>Natija:</b> {correct}/{total} ({score:.1f}%)
"""
        admin_ids = get_admin_ids()
        for admin_id in admin_ids:
            try:
                await bot.send_message(
                    chat_id=admin_id,
                    text=message,
                    parse_mode="HTML"
                )
            except Exception as e:
                logger.error(f"Failed to notify admin {admin_id} about test: {e}")
    except Exception as e:
        logger.error(f"Failed to notify admins about test: {e}")
