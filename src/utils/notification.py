import os
import asyncio
from aiogram import Bot
from dotenv import load_dotenv
import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
load_dotenv()

# Загружаем переменные окружения
TELEGRAM_API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
TELEGRAM_USER_ID = os.getenv("TELEGRAM_USER_ID")

bot = Bot(token=TELEGRAM_API_TOKEN) if TELEGRAM_API_TOKEN else None
#Для отправки в телеграм
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

async def notify_admin(message: str):
    """Функция отправки уведомления через Telegram пользователю по ID."""
    await send_telegram_notification(message)

#Для отправки на почту
# Конфигурация SMTP
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = os.getenv("SMTP_PORT")  # Порт по умолчанию 587
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")


def email_notification(subject: str, message: str):
    """Отправка email-уведомления."""
    if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
        print("[ERROR] Email не настроен. Проверьте EMAIL_ADDRESS и EMAIL_PASSWORD.")
        return
    if not ADMIN_EMAIL:
        print("[ERROR] Email получателя не указан. Проверьте ADMIN_EMAIL.")
        return

    msg = MIMEMultipart()
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = ADMIN_EMAIL
    msg["Subject"] = subject
    msg.attach(MIMEText(message, "plain"))

    server = None
    try:
        print("[INFO] Подключение к SMTP-серверу...")
        server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)  # Используем SSL
        server.ehlo()  # Проверка соединения
        print("[INFO] Аутентификация...")
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)  # Аутентификация
        print("[INFO] Отправка сообщения...")
        server.send_message(msg)  # Отправка сообщения
        print("[INFO] Уведомление на email успешно отправлено.")
    except smtplib.SMTPException as smtp_error:
        print(f"[ERROR] SMTP ошибка: {smtp_error}")
    except Exception as e:
        print(f"[ERROR] Не удалось отправить email: {e}")
    finally:
        if server:
            try:
                server.quit()  # Закрываем соединение
                print("[INFO] Соединение закрыто.")
            except Exception as quit_error:
                print(f"[ERROR] Не удалось закрыть соединение: {quit_error}")
