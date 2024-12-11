from aiogram import Bot, Dispatcher, Router
from aiogram.types import BotCommand, Message, ContentType
from dotenv import load_dotenv
from aiogram.filters import Command
from DB_base.db import init_db
from handlers.welcome import welcome
from handlers.start import collect_user_data
from handlers.contact import handle_contact
import os
import asyncio

load_dotenv()

# Инициализация бота и диспетчера
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

router = Router()

# Регистрируем обработчики через Router
@router.message(Command(commands=["start"]))
async def start_handler(message: Message):
    await welcome(message)

@router.message(lambda message: message.text == "Начать")
async def collect_data_handler(message: Message):
    await collect_user_data(message)

@router.message(lambda message: message.content_type == ContentType.CONTACT)
async def contact_handler(message: Message):
    await handle_contact(message)


async def set_bot_commands():
    """
    Устанавливаем команды, которые будут доступны в меню Telegram.
    """
    commands = [
        BotCommand(command="/start", description="Запустить бота"),
    ]
    await bot.set_my_commands(commands)


async def on_startup():
    """
    Действия при запуске бота.
    """
    print("Инициализация базы данных...")
    await set_bot_commands()


async def main():
    """
    Основная функция запуска бота.
    """
    # Инициализация базы данных
    await init_db()
    await set_bot_commands()
    dp.include_router(router)
    print("Бот успешно запущен. Ожидание сообщений...")

    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Бот остановлен.")