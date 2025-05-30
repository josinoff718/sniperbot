from sniper.database import init_db
from sniper.telegram_bot import telegram_command_loop, send_telegram_message

# Init DB and send startup message
init_db()
send_telegram_message("✅ Bot started. Listening for commands...")

# Start polling only ONCE
bot = telegram_command_loop()
bot.infinity_polling()
