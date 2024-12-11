from aiogram import types
from DB_base.db import get_db, User

async def handle_contact(message: types.Message):
    """
    Обрабатывает контактные данные (номер телефона).
    """
    contact = message.contact

    if contact:
        async for db in get_db():
            try:
                # Проверяем, есть ли пользователь в базе данных
                result = await db.execute(
                    User.__table__.select().where(User.telegram_id == contact.user_id)
                )
                user = result.scalar_one_or_none()

                if user:
                    # Обновляем номер телефона пользователя
                    await db.execute(
                        User.__table__.update()
                        .where(User.telegram_id == contact.user_id)
                        .values(phone_number=contact.phone_number)
                    )
                    await db.commit()

                    # Отправляем уведомление об успешном сохранении
                    await message.answer("Спасибо! Ваш номер телефона успешно сохранён. 📞")
                else:
                    # Пользователь не найден
                    await message.answer("Произошла ошибка: пользователь не найден.")
            except Exception as e:
                # Логируем и отправляем сообщение об ошибке
                await message.answer("Произошла ошибка при сохранении номера телефона.")
                print("Ошибка обновления телефона:", e)