import os
import asyncio
from aiogram import Bot
from dotenv import load_dotenv

load_dotenv()

# Загружаем переменные окружения
TELEGRAM_API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
TELEGRAM_USER_ID = os.getenv("TELEGRAM_USER_ID")

bot = Bot(token=TELEGRAM_API_TOKEN) if TELEGRAM_API_TOKEN else None

async def send_telegram_notification(message: str):
    """Отправка уведомления в Telegram пользователю по ID."""
    if not bot:
        print("[ERROR] Telegram Bot не инициализирован. Проверьте TELEGRAM_API_TOKEN.")
        return
    if not TELEGRAM_USER_ID:
        print("[ERROR] Telegram User ID не задан. Проверьте TELEGRAM_USER_ID.")
        return

    try:
        await bot.send_message(TELEGRAM_USER_ID, message)
        print("[INFO] Уведомление в Telegram успешно отправлено.")
    except Exception as e:
        print(f"[ERROR] Не удалось отправить сообщение в Telegram: {e}")

def notify_admin(message: str):
    """Функция отправки уведомления через Telegram пользователю по ID."""
    asyncio.run(send_telegram_notification(message))

    