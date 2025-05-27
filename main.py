import os
import time

PRIVATE_KEY = os.getenv("PRIVATE_KEY")
WALLET_ADDRESS = os.getenv("WALLET_ADDRESS")
DAILY_LIMIT = float(os.getenv("DAILY_LIMIT", "30"))

print("Real Trading Bot started...")
print(f"Wallet: {WALLET_ADDRESS}")
print(f"Daily Limit: ${DAILY_LIMIT}")

# Simulation loop — replace with actual buy/sell logic
spent = 0
while True:
    if spent < DAILY_LIMIT:
        print("Simulating buy trade...")
        spent += 5  # simulate $5 per trade
        time.sleep(10)
        print("Simulating sell trade...")
        time.sleep(10)
    else:
        print("Daily limit reached. Waiting for next cycle.")
        time.sleep(60)
