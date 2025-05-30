import threading
from sniper.telegram_bot import telegram_command_loop, send_telegram_message

send_telegram_message("✅ Bot started. Listening for commands.")
threading.Thread(target=telegram_command_loop, daemon=True).start()

# Start your SniperBot or main loop here
while True:
    pass