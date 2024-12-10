from telegram import Update
from telegram.ext import ContextTypes
from DB_base.db import get_db, User

def handle_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Обрабатывает контактные данные (номер телефона).
    """
    contact = update.message.contact
    chat_id = update.effective_chat.id

    if contact:
        for db in get_db():
            try:
                # Обновляем номер телефона пользователя
                user = db.query(User).filter(User.telegram_id == contact.user_id).first()
                if user:
                    user.phone_number = contact.phone_number
                    db.commit()

                    context.bot.send_message(
                        chat_id=chat_id,
                        text="Спасибо! Ваш номер телефона успешно сохранён. 📞"
                    )
                else:
                    context.bot.send_message(
                        chat_id=chat_id,
                        text="Произошла ошибка: пользователь не найден."
                    )
            except Exception as e:
                context.bot.send_message(
                    chat_id=chat_id,
                    text="Произошла ошибка при сохранении номера телефона."
                )
                print("Ошибка обновления телефона:", e)