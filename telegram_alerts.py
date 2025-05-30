import os
import requests

class TelegramBot:
    def __init__(self):
        self.token = os.getenv("TELEGRAM_TOKEN")
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID")

    def send(self, message):
        if not self.token or not self.chat_id:
            return
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        data = {"chat_id": self.chat_id, "text": message}
        try:
            requests.post(url, data=data)
        except Exception as e:
            print(f"[BOT] Telegram error: {e}")
