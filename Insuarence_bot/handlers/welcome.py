from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

async def welcome(message: types.Message):
    """"
    Отправляет приветственное сообщение новому пользователю.
    """
    user = message.from_user.first_name

    text = (
        f"Здравствуйте, {user}! 👋\n"
        "Я помогу вам оформить автомобильную страховку быстро и удобно.\n"
        "Начнём? Для этого мне потребуется немного информации."
    )
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Начать")]  # Одна кнопка в строке
        ],
        resize_keyboard=True  # Уменьшить клавиатуру под размер кнопок
    )

    await message.answer(text, reply_markup=keyboard)
