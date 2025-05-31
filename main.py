from sniper.database import init_db, seed_wallets
from sniper.telegram_bot import telegram_command_loop, send_telegram_message
from sniper.bot import SniperBot

init_db()
seed_wallets()
send_telegram_message("✅ SniperBot started. Running live trades + listening for commands...")
SniperBot().run()
telegram_command_loop()