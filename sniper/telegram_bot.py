import os
import requests
import json

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

def handle_command(message_text):
    if message_text.startswith("/limit"):
        try:
            _, amount = message_text.split()
            value = int(amount)
            save_daily_limit(value)
            return f"✅ Daily USD limit updated to ${value}"
        except:
            return "❌ Usage: /limit [amount]"

    elif message_text.startswith("/wallets"):
        # Example static wallet list for now
        return (
            "📡 Tracked Wallets:
"
            "- Tier 1: 9Rqb3N..., BQ9BX1...
"
            "- Tier 2: 7bCzMy..., 5ZsZm5...
"
            "- Tier 3: EusCkS..., 5aE1AY..."
        )

    elif message_text.startswith("/report"):
        from sniper.utils import generate_daily_report
        return generate_daily_report()

    return "🤖 Unknown command. Try /limit, /wallets, or /report"