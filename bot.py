import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

# ======================================
# ==== ТВОЙ ТОКЕН ======================
# ======================================
TELEGRAM_TOKEN = '8451839561:AAGOa2BqD47DUwufli6kYYAWPjK_rHyIAck'
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# ======================================
# ==== УСТАНОВКА КНОПКИ МЕНЮ ===========
# ======================================
def set_menu_button():
    try:
        bot.set_chat_menu_button(
            menu_button={
                "type": "web_app",
                "text": "🚀 Открыть",
                "web_app": {
                    "url": "https://lololopanton.github.io/webapp/"
                }
            }
        )
        print("✅ Кнопка меню установлена глобально")
    except Exception as e:
        print(f"Ошибка установки кнопки: {e}")

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
    print("✅ Бот запущен (финальная версия)")
    print("🌐 Web App: https://lololopanton.github.io/webapp/")
    
    # Устанавливаем кнопку меню
    set_menu_button()
    
    # Бесконечный цикл с защитой от падений
    import time
    while True:
        try:
            bot.polling(none_stop=True, interval=0, timeout=20)
        except Exception as e:
            print(f"❌ Ошибка: {e}")
            time.sleep(5)
            print("🔄 Перезапуск...")