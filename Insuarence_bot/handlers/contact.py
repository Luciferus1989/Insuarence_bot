from telegram import Update
from telegram.ext import ContextTypes
from DB_base.db import get_db, User

async def handle_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Обрабатывает контактные данные (номер телефона).
    """
    contact = update.message.contact
    chat_id = update.effective_chat.id

    if contact:
        async for db in get_db():
            try:
                result = await db.execute(
                    User.__table__.select().where(User.telegram_id == contact.user_id)
                )
                user = result.scalar_one_or_none()
                if user:
                    await db.execute(
                        User.__table__.update()
                        .where(User.telegram_id == contact.user_id)
                        .values(phone_number=contact.phone_number)
                    )
                    await db.commit()
                    await context.bot.send_message(
                        chat_id=chat_id,
                        text="Спасибо! Ваш номер телефона успешно сохранён. 📞"
                    )
                else:
                    await context.bot.send_message(
                        chat_id=chat_id,
                        text="Произошла ошибка: пользователь не найден."
                    )
            except Exception as e:
                await context.bot.send_message(
                    chat_id=chat_id,
                    text="Произошла ошибка при сохранении номера телефона."
                )
                print("Ошибка обновления телефона:", e)