import os
import requests
import json
import time
import telebot

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
DAILY_LIMIT_FILE = "daily_limit.json"

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
        bot.send_message(message.chat.id, "📊 PnL report placeholder.")  # Replace with actual logic

    while True:
        try:
            bot.polling()
        except Exception as e:
            print(f"Telegram polling error: {e}")
            time.sleep(5)