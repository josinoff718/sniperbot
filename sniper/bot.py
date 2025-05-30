from sniper.telegram_bot import send_telegram_message

class SniperBot:
    def __init__(self):
        send_telegram_message("✅ SniperBot initialized and ready.")

    def run(self):
        send_telegram_message("🚀 SniperBot running live trading loop.")
        # Placeholder for main loop logic