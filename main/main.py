from sniper.database import init_db
from sniper.telegram_bot import telegram_command_loop, send_telegram_message
from sniper.bot import SniperBot

init_db()
send_telegram_message("✅ SniperBot started. Running live trades + listening for commands...")
SniperBot().run()
telegram_command_loop()
 
 
 
