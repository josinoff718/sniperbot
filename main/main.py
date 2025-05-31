from sniper.database import init_db
from sniper.telegram_bot import telegram_command_loop, send_telegram_message
from sniper.bot import SniperBot

# Step 1: Initialize the database
init_db()

# Step 2: Send Telegram startup confirmation
send_telegram_message("✅ SniperBot started. Running live trades + listening for commands...")

# Step 3: Start the sniper bot (live trading loop)
SniperBot().run()

# Step 4: Start Telegram command loop
telegram_command_loop()
 
 
