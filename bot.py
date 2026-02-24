import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

TELEGRAM_TOKEN = '8451839561:AAGOa2BqD47DUwufli6kYYAWPjK_rHyIAck'
bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    username = message.from_user.username or 'NoUsername'
    markup = InlineKeyboardMarkup()
    button = InlineKeyboardButton(
        text="🚀 Открыть приложение",
        web_app=WebAppInfo(url="https://lololopanton.github.io/webapp/")
    )
    markup.add(button)
    bot.send_message(
        message.chat.id,
        f"👋 Привет, @{username}!\n\nНажми кнопку ниже:",
        reply_markup=markup
    )

if __name__ == "__main__":
    print("✅ Бот запущен")
    bot.polling(none_stop=True)
