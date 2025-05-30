from sniper.database import init_db
from sniper.telegram_bot import telegram_command_loop, send_telegram_message

# Step 1: Initialize the database
init_db()

# Step 2: Insert a dummy trade
import sqlite3
conn = sqlite3.connect("trades.db")
c = conn.cursor()
c.execute("INSERT INTO trades (wallet, token, amount, buy_price, sell_price, profit) VALUES (?, ?, ?, ?, ?, ?)",
          ("TESTWALLET", "TESTTOKEN", 1.0, 0.5, 1.0, 0.5))
conn.commit()
conn.close()
print("✅ Inserted dummy trade for testing.")

# Step 3: Notify bot start
send_telegram_message("✅ Bot started. Listening for commands...")

# Step 4: Start Telegram polling
telegram_command_loop()
