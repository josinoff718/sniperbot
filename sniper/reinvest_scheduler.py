import schedule
import time
from sniper.reinvest import auto_reinvest
from sniper.telegram_bot import send_telegram_message

def reinvest_task():
    result = auto_reinvest()
    send_telegram_message(f"🔁 Auto-reinvest complete:\n{result}")

schedule.every().day.at("00:10").do(reinvest_task)

print("⏰ Reinvest scheduler running...")

while True:
    schedule.run_pending()
    time.sleep(30)