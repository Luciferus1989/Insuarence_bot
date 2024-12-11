from aiogram import Bot, Dispatcher, Router
from aiogram.types import BotCommand, Message
from aiogram.utils import executor
from dotenv import load_dotenv
from handlers.welcome import welcome
from handlers.start import collect_user_data
from handlers.contact import handle_contact
import os

load_dotenv()

# Инициализация бота и диспетчера
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

router = Router()

# Регистрируем обработчики через Router
@router.message(commands=["start"])
async def start_handler(message: Message):
    await welcome(message)

@router.message(lambda message: message.text == "Начать")
async def collect_data_handler(message: Message):
    await collect_user_data(message)

@router.message(content_types=["contact"])
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
    print("Бот запущен. Ожидание сообщений...")


def main():
    """
    Основная функция для запуска бота.
    """
    dp.include_router(router)
    executor.run(dp, bot=bot, on_startup=on_startup)


if __name__ == "__main__":
    main()