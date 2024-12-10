from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext

def welcome(update: Update, context: CallbackContext) -> None:
    """"
    Отправляет приветственное сообщение новому пользователю.
    """
    user = update.effective_user
    chat_id = update.effective_chat.id
    message = (
        f"Здравствуйте, {user.first_name}! 👋\n"
        "Я помогу вам оформить автомобильную страховку быстро и удобно.\n"
        "Начнём? Для этого мне потребуется немного информации."
    )
    keyboard = [
        ["Начать"],
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    context.bot.send_message(
        chat_id=chat_id,
        text=message,
        reply_markup=reply_markup,
    )
