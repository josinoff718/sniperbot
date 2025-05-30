from sniper.database import init_db
from sniper.telegram_bot import telegram_command_loop, send_telegram_message

init_db()
send_telegram_message("✅ Bot started. Listening for commands...")
bot = telegram_command_loop()
bot.infinity_polling()
