from telegram import Update, ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes
from telegram.ext import CallbackContext
from DB_base.db import get_db, User


def collect_user_data(update: Update, context: CallbackContext):
    """
    Собирает данные о пользователе и сохраняет их в базу данных.
    """
    user = update.effective_user
    chat_id = update.effective_chat.id
    # Данные о пользователе
    user_data = {
        "telegram_id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "username": user.username,
        "language_code": user.language_code,
    }
    # Получаем сессию базы
    for db in get_db():
        try:
            # Проверяем, есть ли пользователь
            existing_user = db.query(User).filter(User.telegram_id == user.id).first()
            if not existing_user:
                new_user = User(**user_data)
                db.add(new_user)
                db.commit()

                context.bot.send_message(
                    chat_id=chat_id,
                    text="Ваши данные успешно сохранены! 🚗",
                    reply_markup=ReplyKeyboardRemove(),
                )
                context.bot.send_message(
                    chat_id=chat_id,
                    text="Нам может потребоваться ваш номер телефона!\n"
                         "(Мы не будем спамить на него, честно-честно!)",
                )
                keyboard = [[KeyboardButton("Отправить номер телефона", request_contact=True)]]
                reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
                context.bot.send_message(
                    chat_id=chat_id,
                    text="Телефон:",
                    reply_markup=reply_markup,
                )
            else:
                keyboard = [
                    ["Check profile"],
                ]
                reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
                context.bot.send_message(
                    chat_id=chat_id,
                    text="Вы уже зарегистрированы! 🚗",
                    reply_markup=reply_markup,
                )
        except Exception as e:
            context.bot.send_message(
                chat_id=chat_id,
                text="Произошла ошибка при сохранении данных. Попробуйте позже.",
            )
            print("Ошибка сохранения в базу:", e)