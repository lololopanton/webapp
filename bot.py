import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

# ======================================
# ==== ТВОЙ ТОКЕН ======================
# ======================================
TELEGRAM_TOKEN = '8451839561:AAGOa2BqD47DUwufli6kYYAWPjK_rHyIAck'
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# ======================================
# ==== КОМАНДА /START ==================
# ======================================
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    username = message.from_user.username or 'NoUsername'
    
    # Создаём кнопку для Web App
    markup = InlineKeyboardMarkup()
    web_app_url = "https://lololopanton.github.io/webapp/"
    
    button = InlineKeyboardButton(
        text="🚀 Открыть приложение",
        web_app=WebAppInfo(url=web_app_url)
    )
    markup.add(button)
    
    # Отправляем сообщение
    bot.send_message(
        user_id, 
        f"👋 Привет, @{username}!\n\n"
        f"Нажми кнопку ниже, чтобы открыть приложение:",
        reply_markup=markup
    )

# ======================================
# ==== ЗАПУСК БОТА =====================
# ======================================
if __name__ == "__main__":
    print("✅ Бот запущен (упрощённая версия)")
    print("🌐 Web App: https://lololopanton.github.io/webapp/")
    
    while True:
        try:
            bot.polling(none_stop=True, interval=0, timeout=20)
        except Exception as e:
            print(f"❌ Ошибка: {e}")
            import time
            time.sleep(5)
            print("🔄 Перезапуск...")