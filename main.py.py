from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sqlite3

# ======================================
# ==== СОЗДАЁМ СЕРВЕР ==================
# ======================================
app = FastAPI()

# Разрешаем запросы с твоего сайта
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://lololopanton.github.io"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ======================================
# ==== БАЗА ДАННЫХ =====================
# ======================================
conn = sqlite3.connect('balances.db', check_same_thread=False)
cursor = conn.cursor()

# Создаём таблицу для балансов пользователей
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id TEXT PRIMARY KEY,
        balance INTEGER DEFAULT 0
    )
''')
conn.commit()

# ======================================
# ==== ПОЛУЧИТЬ БАЛАНС =================
# ======================================
@app.get("/balance/{user_id}")
def get_balance(user_id: str):
    cursor.execute("SELECT balance FROM users WHERE user_id=?", (user_id,))
    result = cursor.fetchone()
    
    if result:
        balance = result[0]
    else:
        # Если пользователя нет, создаём с 0
        cursor.execute("INSERT INTO users (user_id, balance) VALUES (?, 0)", (user_id,))
        conn.commit()
        balance = 0
    
    return {"balance": balance}

# ======================================
# ==== ДОБАВИТЬ БАЛАНС =================
# ======================================
@app.post("/balance/{user_id}/add/{amount}")
def add_balance(user_id: str, amount: int):
    # Проверяем, есть ли пользователь
    cursor.execute("SELECT balance FROM users WHERE user_id=?", (user_id,))
    result = cursor.fetchone()
    
    if result:
        # Обновляем баланс
        new_balance = result[0] + amount
        cursor.execute("UPDATE users SET balance = ? WHERE user_id=?", (new_balance, user_id))
    else:
        # Создаём нового пользователя
        new_balance = amount
        cursor.execute("INSERT INTO users (user_id, balance) VALUES (?, ?)", (user_id, new_balance))
    
    conn.commit()
    return {"balance": new_balance}

# ======================================
# ==== ПРОВЕРКА СЕРВЕРА =================
# ======================================
@app.get("/")
def root():
    return {
        "status": "online",
        "message": "Balance server is running"
    }
