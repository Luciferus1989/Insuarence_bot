import os
import asyncio
from telegram.ext import Application, MessageHandler, filters, CommandHandler
from dotenv import load_dotenv
from telegram import Update
from DB_base.db import init_db
from handlers import welcome, start, contact

load_dotenv()

async def echo(update: Update, context):
    """Обработчик для эхо-ответа."""
    await update.message.reply_text(update.message.text)

def main():
    """Запуск бота."""
    application = Application.builder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()

    # Добавляем обработчик сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    print("Бот запущен. Ожидание сообщений...")
    application.run_polling()

if __name__ == "__main__":
    main()

# async def run_bot():
#     """Асинхронная точка входа для бота."""
#     # Инициализируем базу данных
#     await init_db()
#
#     # Создаём объект приложения Telegram Bot API
#     application = Application.builder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()
#
#     # Добавляем хендлеры
#     application.add_handler(CommandHandler("start", welcome.welcome))
#     application.add_handler(MessageHandler(filters.TEXT & filters.Regex("^Начать$"), start.collect_user_data))
#     application.add_handler(MessageHandler(filters.CONTACT, contact.handle_contact))
#
#     # Запуск бота
#     print("Бот запущен. Ожидание сообщений...")
#     await application.run_polling()
#
# if __name__ == "__main__":
#     try:
#         # Проверяем, есть ли активный цикл событий
#         loop = asyncio.get_event_loop()
#     except RuntimeError:  # Если цикла нет, создаём новый
#         loop = asyncio.new_event_loop()
#         asyncio.set_event_loop(loop)
#
#     loop.run_until_complete(run_bot())