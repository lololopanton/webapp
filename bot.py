import telebot
import sqlite3
import time
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

# ======================================
# ==== ТВОЙ ТОКЕН ======================
# ======================================
TELEGRAM_TOKEN = '8451839561:AAGOa2BqD47DUwufli6kYYAWPjK_rHyIAck'
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# ======================================
# ==== БАЗА ДАННЫХ =====================
# ======================================
conn = sqlite3.connect('users.db', check_same_thread=False)
cursor = conn.cursor()

# Создаём таблицу пользователей (ТОЛЬКО user_id и balance)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        balance INTEGER DEFAULT 0
    )
''')
conn.commit()

# ======================================
# ==== ФУНКЦИЯ ОБНОВЛЕНИЯ КНОПКИ МЕНЮ ===
# ======================================
def update_menu_button(user_id):
    try:
        cursor.execute("SELECT balance FROM users WHERE user_id=?", (user_id,))
        result = cursor.fetchone()
        balance = result[0] if result else 0
        
        # Создаём кнопку меню с актуальным балансом
        menu_button = {
            "type": "web_app",
            "text": f"💰 {balance} USDT",
            "web_app": {
                "url": f"https://lololopanton.github.io/webapp/?balance={balance}"
            }
        }
        
        # Устанавливаем кнопку меню для этого пользователя
        bot.set_chat_menu_button(chat_id=user_id, menu_button=menu_button)
        print(f"✅ Кнопка обновлена для {user_id}: {balance} USDT")
    except Exception as e:
        print(f"Ошибка обновления кнопки: {e}")

# ======================================
# ==== КОМАНДА /START ==================
# ======================================
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    username = message.from_user.username or 'NoUsername'
    
    # Добавляем пользователя в базу (ТОЛЬКО user_id)
    cursor.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
    conn.commit()
    
    # Получаем баланс пользователя
    cursor.execute("SELECT balance FROM users WHERE user_id=?", (user_id,))
    balance = cursor.fetchone()[0]
    
    # Создаём кнопку с передачей баланса в URL
    markup = InlineKeyboardMarkup()
    web_app_url = f"https://lololopanton.github.io/webapp/?balance={balance}"
    
    button = InlineKeyboardButton(
        text="🚀 Открыть приложение",
        web_app=WebAppInfo(url=web_app_url)
    )
    markup.add(button)
    
    # Отправляем сообщение
    bot.send_message(
        user_id, 
        f"👋 Привет, @{username}!\n\n"
        f"💰 Твой баланс: {balance} USDT\n\n"
        f"Нажми кнопку ниже, чтобы открыть приложение:",
        reply_markup=markup
    )
    
    # Обновляем кнопку меню
    update_menu_button(user_id)

# ======================================
# ==== КОМАНДА /BALANCE ================
# ======================================
@bot.message_handler(commands=['balance'])
def balance(message):
    user_id = message.chat.id
    cursor.execute("SELECT balance FROM users WHERE user_id=?", (user_id,))
    result = cursor.fetchone()
    balance = result[0] if result else 0
    bot.send_message(user_id, f"💰 Твой баланс: {balance} USDT")
    
    # Обновляем кнопку меню
    update_menu_button(user_id)

# ======================================
# ==== КОМАНДА /DEPOSIT ================
# ======================================
@bot.message_handler(commands=['deposit'])
def deposit(message):
    user_id = message.chat.id
    bot.send_message(
        user_id, 
        "📥 Адрес для пополнения:\n"
        "`TTestAddress123456789`\n\n"
        "После отправки нажми /check", 
        parse_mode='Markdown'
    )

# ======================================
# ==== КОМАНДА /CHECK ==================
# ======================================
@bot.message_handler(commands=['check'])
def check(message):
    user_id = message.chat.id
    msg = bot.send_message(user_id, "⏳ Проверяю платеж...")
    time.sleep(2)
    
    # Начисляем тестовые 100 USDT
    cursor.execute("UPDATE users SET balance = balance + 100 WHERE user_id=?", (user_id,))
    conn.commit()
    
    # Получаем новый баланс
    cursor.execute("SELECT balance FROM users WHERE user_id=?", (user_id,))
    new_balance = cursor.fetchone()[0]
    
    bot.edit_message_text(
        f"✅ Начислено 100 USDT!\n"
        f"💰 Новый баланс: {new_balance} USDT", 
        user_id, 
        msg.message_id
    )
    
    # Обновляем кнопку меню
    update_menu_button(user_id)

# ======================================
# ==== КОМАНДА /WITHDRAW ===============
# ======================================
@bot.message_handler(commands=['withdraw'])
def withdraw(message):
    try:
        parts = message.text.split()
        if len(parts) != 3:
            bot.send_message(
                message.chat.id, 
                "❌ Формат: /withdraw <сумма> <адрес>\n"
                "Пример: /withdraw 50 TTestAddress123"
            )
            return
        
        amount = float(parts[1])
        address = parts[2]
        user_id = message.chat.id
        
        cursor.execute("SELECT balance FROM users WHERE user_id=?", (user_id,))
        result = cursor.fetchone()
        balance = result[0] if result else 0
        
        if balance < amount:
            bot.send_message(user_id, "❌ Недостаточно средств")
            return
        
        # Списываем средства
        cursor.execute("UPDATE users SET balance = balance - ? WHERE user_id=?", (amount, user_id))
        conn.commit()
        
        # Получаем новый баланс
        cursor.execute("SELECT balance FROM users WHERE user_id=?", (user_id,))
        new_balance = cursor.fetchone()[0]
        
        bot.send_message(
            user_id, 
            f"✅ Вывод {amount} USDT на адрес {address} (тестовый)\n"
            f"💰 Новый баланс: {new_balance} USDT"
        )
        
        # Обновляем кнопку меню
        update_menu_button(user_id)
        
    except ValueError:
        bot.send_message(message.chat.id, "❌ Сумма должна быть числом")
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Ошибка: {e}")

# ======================================
# ==== КОМАНДА /APP ====================
# ======================================
@bot.message_handler(commands=['app'])
def app(message):
    user_id = message.chat.id
    
    # Получаем баланс
    cursor.execute("SELECT balance FROM users WHERE user_id=?", (user_id,))
    balance = cursor.fetchone()[0]
    
    markup = InlineKeyboardMarkup()
    web_app_url = f"https://lololopanton.github.io/webapp/?balance={balance}"
    
    button = InlineKeyboardButton(
        text="🚀 Открыть приложение",
        web_app=WebAppInfo(url=web_app_url)
    )
    markup.add(button)
    
    bot.send_message(
        message.chat.id, 
        f"💰 Твой баланс: {balance} USDT\n\nНажми кнопку, чтобы открыть приложение:", 
        reply_markup=markup
    )
    
    # Обновляем кнопку меню
    update_menu_button(user_id)

# ======================================
# ==== ОБРАБОТКА ДАННЫХ ИЗ WEB APP =====
# ======================================
@bot.message_handler(content_types=['web_app_data'])
def handle_web_app_data(message):
    user_id = message.chat.id
    import json
    
    try:
        # Получаем данные из Web App
        data = json.loads(message.web_app_data.data)
        action = data.get('action')
        print(f"Получен запрос: {action} от {user_id}")
        
        if action == 'get_balance':
            # Запрос баланса
            cursor.execute("SELECT balance FROM users WHERE user_id=?", (user_id,))
            result = cursor.fetchone()
            balance = result[0] if result else 0
            
            # Отправляем баланс обратно
            bot.send_message(user_id, f"💰 Текущий баланс: {balance} USDT")
            
        elif action == 'withdraw':
            amount = float(data.get('amount', 0))
            address = data.get('address', '')
            
            cursor.execute("SELECT balance FROM users WHERE user_id=?", (user_id,))
            result = cursor.fetchone()
            balance = result[0] if result else 0
            
            if balance >= amount:
                cursor.execute("UPDATE users SET balance = balance - ? WHERE user_id=?", (amount, user_id))
                conn.commit()
                
                cursor.execute("SELECT balance FROM users WHERE user_id=?", (user_id,))
                new_balance = cursor.fetchone()[0]
                
                bot.send_message(
                    user_id, 
                    f"✅ Вывод {amount} USDT на {address}\n"
                    f"💰 Новый баланс: {new_balance} USDT"
                )
                
                # Обновляем кнопку меню
                update_menu_button(user_id)
            else:
                bot.send_message(user_id, "❌ Недостаточно средств")
                
        elif action == 'send':
            amount = float(data.get('amount', 0))
            address = data.get('address', '')
            bot.send_message(user_id, f"✈️ Отправка {amount} USDT на {address} (тест)")
            
    except Exception as e:
        bot.send_message(user_id, f"❌ Ошибка: {e}")
        print(f"Ошибка обработки web_app_data: {e}")

# ======================================
# ==== ЗАПУСК БОТА =====================
# ======================================
if __name__ == "__main__":
    print("✅ Бот запущен!")
    print(f"📊 База данных: users.db")
    print(f"🌐 Web App: https://lololopanton.github.io/webapp/")
    print("💰 Кнопка меню будет обновляться автоматически")
    
    # Бесконечный цикл с обработкой ошибок
    while True:
        try:
            bot.polling(none_stop=True, interval=0, timeout=20)
        except Exception as e:
            print(f"❌ Ошибка соединения: {e}")
            time.sleep(5)
            print("🔄 Перезапуск бота...")