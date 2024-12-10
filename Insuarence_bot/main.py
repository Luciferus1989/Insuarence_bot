import os
from telegram.ext import Application, MessageHandler, filters, CommandHandler
from dotenv import load_dotenv
from DB_base.db import init_db
from handlers import welcome, start, contact

load_dotenv()


def run_bot():
    """Точка входа для бота."""

    # Инициализируем базу данных
    init_db()

    # Создаём объект приложения Telegram Bot API
    application = Application.builder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()

    # Добавляем хендлеры
    application.add_handler(CommandHandler("start", welcome.welcome))
    application.add_handler(MessageHandler(filters.TEXT & filters.Regex("^Начать$"), start.collect_user_data))
    application.add_handler(MessageHandler(filters.CONTACT, contact.handle_contact))

    # Запуск бота
    application.run_polling()

if __name__ == "__main__":
    try:
        run_bot()
    except Exception as e:
        print(f"Произошла ошибка: {e}")
    except KeyboardInterrupt:
        print("Завершение работы бота.")