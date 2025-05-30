 
import os
import requests
import json
import time
import telebot
import sqlite3
from datetime import datetime

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
DAILY_LIMIT_FILE = "daily_limit.json"
DB_PATH = "pnl_tracking.db"

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }
    requests.post(url, json=payload)

def save_daily_limit(value):
    with open(DAILY_LIMIT_FILE, "w") as f:
        json.dump({"usd_limit": value}, f)

def load_daily_limit():
    if os.path.exists(DAILY_LIMIT_FILE):
        with open(DAILY_LIMIT_FILE, "r") as f:
            return json.load(f).get("usd_limit", 30)
    return 30

def log_trade(token, profit_usd, outcome):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS trades (
                    id INTEGER PRIMARY KEY,
                    token TEXT,
                    profit_usd REAL,
                    outcome TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )''')
    c.execute("INSERT INTO trades (token, profit_usd, outcome) VALUES (?, ?, ?)", (token, profit_usd, outcome))
    conn.commit()
    conn.close()

def get_daily_report():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    today = datetime.utcnow().date()
    start = datetime.combine(today, datetime.min.time())
    end = datetime.combine(today, datetime.max.time())

    c.execute("SELECT token, profit_usd, outcome FROM trades WHERE timestamp BETWEEN ? AND ?", (start, end))
    rows = c.fetchall()
    conn.close()

    if not rows:
        return "📊 No trades recorded today."

    total_profit = sum(row[1] for row in rows)
    wins = sum(1 for row in rows if row[2] == "win")
    losses = sum(1 for row in rows if row[2] == "loss")
    win_rate = (wins / len(rows)) * 100 if rows else 0

    top_token = max(rows, key=lambda r: r[1])[0] if rows else "N/A"

    return (f"📊 Daily PnL Summary ({today.strftime('%b %d')})\n"
            f"Profit: ${total_profit:.2f}\n"
            f"Trades: {len(rows)} ({wins} win / {losses} loss)\n"
            f"Win Rate: {win_rate:.0f}%\n"
            f"Top Token: ${top_token}")

def telegram_command_loop():
    bot = telebot.TeleBot(TELEGRAM_TOKEN)

    @bot.message_handler(commands=['wallets'])
    def handle_wallets(message):
        bot.send_message(message.chat.id, "📡 Tracked Wallets:\n- Tier 1: 9Rqb3N..., BQ9BX1...\n- Tier 2: 7bCzMy..., 5ZsZm5...\n- Tier 3: EusCkS..., 5aE1AY...")

    @bot.message_handler(commands=['limit'])
    def handle_limit(message):
        limit = load_daily_limit()
        bot.send_message(message.chat.id, f"💰 Daily Limit: ${limit} USD")

    @bot.message_handler(commands=['report'])
    def handle_report(message):
    try:
        report = get_daily_report()
        bot.send_message(message.chat.id, report)
    except Exception as e:
        bot.send_message(message.chat.id, f"⚠️ Error in /report: {str(e)}")
 

    print("✅ Telegram command listener started.")

    # ✅ This line starts polling in a thread-safe way
    bot.infinity_polling()
 

    @bot.message_handler(commands=['wallets'])
    def handle_wallets(message):
        bot.send_message(message.chat.id, "📡 Tracked Wallets:\n- Tier 1: 9Rqb3N..., BQ9BX1...\n- Tier 2: 7bCzMy..., 5ZsZm5...\n- Tier 3: EusCkS..., 5aE1AY...")

    @bot.message_handler(commands=['limit'])
    def handle_limit(message):
        limit = load_daily_limit()
        bot.send_message(message.chat.id, f"💰 Daily Limit: ${limit} USD")

    @bot.message_handler(commands=['report'])
    def handle_report(message):
        report = get_daily_report()
        bot.send_message(message.chat.id, report)

    while True:
        try:
            bot.polling()
        except Exception as e:
            print(f"Telegram polling error: {e}")
            time.sleep(5)
