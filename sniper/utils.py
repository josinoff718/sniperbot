import os
import requests
import logging
import time
from datetime import datetime

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Telegram
def send_telegram_message(message):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
        requests.post(url, json=payload)
    except Exception as e:
        logging.error(f"Telegram error: {e}")

# CoinGecko
def get_sol_price_usd():
    try:
        res = requests.get("https://api.coingecko.com/api/v3/simple/price", params={
            "ids": "solana",
            "vs_currencies": "usd"
        })
        return res.json()["solana"]["usd"]
    except Exception as e:
        logging.error(f"Failed to fetch SOL price: {e}")
        return 0

def convert_usd_to_sol(usd_amount):
    price = get_sol_price_usd()
    return round(usd_amount / price, 4) if price else 0

# Tiered Strategy
TIER_CONFIG = {
    'tier1': {
        'wallets': [
            "9Rqb3Nvru6Mjtnf8wWh9YFe5dqfeLbGXL6vCn8DdCvTg",
            "BQ9BX1fnN2e2ByskRAybiw21MPtJLUpDY191Cgq3LyKp"
        ],
        'amount_usd': 12,
        'filters': []
    },
    'tier2': {
        'wallets': [
            "7bCzMyCij95vjM73GpSgBvUPaVWfwBVoQgFjysFqivFQ",
            "5ZsZm5pYHqvQG42HDvhoxqH6fXFKKm7AHEw9b43n9S4K",
            "HKhy53MaayQYoB6ZEPiYPkNPLPGMTrnqQv35zQkNyXht"
        ],
        'amount_usd': 8,
        'filters': ['twitter', 'volume']
    },
    'tier3': {
        'wallets': [
            "EusCkSwcwYc8vPfVq69qupxGj1wV4ThTN93onpwhk86z",
            "5aE1AYshLkXWbVaDCnA6ToKMJdeZdXWTzskLUozuhPUU"
        ],
        'amount_usd': 4,
        'filters': ['twitter', 'rugcheck', 'volume', 'age']
    }
}

def get_wallet_tier(wallet_address):
    for tier, config in TIER_CONFIG.items():
        if wallet_address in config['wallets']:
            return tier, config
    return 'unknown', {'amount_usd': 0, 'filters': []}