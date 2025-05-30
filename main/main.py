from sniper.database import init_db
from sniper.telegram_bot import telegram_command_loop 

# Step 1: Initialize the database
init_db()

# Step 2: Send Telegram startup confirmation
send_telegram_message("✅ Bot started. Listening for commands...")

# Step 3: Start polling Telegram commands
telegram_command_loop()
 
