from sniper.database import init_db
from sniper.telegram_bot import telegram_command_loop
from sniper.bot import SniperBot
from sniper.telegram_bot import send_telegram_message

init_db()
send_telegram_message("✅ SniperBot started. Running live trades + listening for commands...")
SniperBot().run()
telegram_command_loop()
