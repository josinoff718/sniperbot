from sniper.database import init_db
from sniper.telegram_bot import telegram_command_loop, send_telegram_message

# Initialize database
init_db()

# Notify start
send_telegram_message("✅ Bot started. Listening for commands...")

# Start the Telegram listener
telegram_command_loop()
 
