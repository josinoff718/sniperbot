import os
import requests

def send_telegram_alert(message):
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if token and chat_id:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        data = {"chat_id": chat_id, "text": message}
        try:
            response = requests.post(url, data=data)
            if response.status_code == 200:
                print("[ALERT] Telegram message sent.")
            else:
                print(f"[ERROR] Telegram failed: {response.text}")
        except Exception as e:
            print(f"[ERROR] Telegram exception: {str(e)}")
    else:
        print("[ERROR] Telegram credentials not set.")
