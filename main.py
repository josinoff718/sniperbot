from sniper.database import init_db
from sniper.telegram_bot import telegram_command_loop, send_telegram_message
from sniper.bot import SniperBot

# Initialize DB
init_db()

# Telegram confirmation
send_telegram_message("✅ SniperBot started. Running live trades + listening for commands...")

# Start bot
SniperBot().run()

# Start Telegram commands
telegram_command_loop()
 
