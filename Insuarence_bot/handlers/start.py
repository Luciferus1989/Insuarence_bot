from aiogram import types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from DB_base.db import get_db, User

async def collect_user_data(message: types.Message):
    """
    Собирает данные о пользователе и сохраняет их в базу данных.
    """
    user_data = {
        "telegram_id": message.from_user.id,
        "first_name": message.from_user.first_name,
        "last_name": message.from_user.last_name,
        "username": message.from_user.username,
        "language_code": message.from_user.language_code,
    }

    async for db in get_db():
        try:
            # Проверяем, есть ли пользователь в базе данных
            result = await db.execute(
                User.__table__.select().where(User.telegram_id == message.from_user.id)
            )
            existing_user = result.scalar_one_or_none()

            if not existing_user:
                # Если пользователя нет, добавляем его
                await db.execute(User.__table__.insert().values(**user_data))
                await db.commit()

                # Уведомляем пользователя об успешной регистрации
                await message.answer(
                    "Ваши данные успешно сохранены! 🚗",
                    reply_markup=ReplyKeyboardRemove(),
                )

                # Просим отправить номер телефона
                keyboard = ReplyKeyboardMarkup(
                    keyboard=[
                        [KeyboardButton(text='Отправить номер телефона', request_contact=True)]
                    ],
                    resize_keyboard=True,
                    one_time_keyboard=True,
                )
                await message.answer(
                    "Нам может потребоваться ваш номер телефона.\n"
                    "(Мы не будем спамить на него, честно-честно!)",
                    reply_markup=keyboard,
                )
            else:
                # Если пользователь уже зарегистрирован
                keyboard = ReplyKeyboardMarkup(
                    keyboard=[[KeyboardButton(text="Check profile")]],
                    resize_keyboard=True,
                )
                await message.answer(
                    "Вы уже зарегистрированы! 🚗",
                    reply_markup=keyboard,
                )
        except Exception as e:
            # Логируем и сообщаем об ошибке
            await message.answer(
                "Произошла ошибка при сохранении данных. Попробуйте позже."
            )
            print(f"Ошибка сохранения в базу: {e}")