import os
import time
import requests

PRIVATE_KEY = os.getenv("PRIVATE_KEY")
WALLET_ADDRESS = os.getenv("WALLET_ADDRESS")
DAILY_LIMIT = float(os.getenv("DAILY_LIMIT", "30"))

spent = 0
JUPITER_QUOTE_URL = "https://quote-api.jup.ag/v6/quote"

def log(msg):
    print(f"[BOT] {msg}", flush=True)

def fetch_trading_opportunity():
    return {"mint": "So11111111111111111111111111111111111111112", "amount": 0.01}  # SOL

def simulate_jupiter_trade(mint, amount):
    try:
        response = requests.get(JUPITER_QUOTE_URL, params={
            "inputMint": "So11111111111111111111111111111111111111112",
            "outputMint": mint,
            "amount": int(amount * 1_000_000_000),
            "slippageBps": 100,
            "onlyDirectRoutes": True
        })
        return response.json()
    except Exception as e:
        log(f"Error querying Jupiter: {e}")
        return None

log("Real Auto-Trader Activated")
log(f"Wallet: {WALLET_ADDRESS} | Daily Limit: ${DAILY_LIMIT}")

while True:
    if spent >= DAILY_LIMIT:
        log("Daily trading limit reached. Sleeping...")
        time.sleep(60)
        continue

    opp = fetch_trading_opportunity()
    if opp:
        mint = opp["mint"]
        amount = opp["amount"]
        log(f"Trigger received: Buy {amount} SOL of {mint}")
        quote = simulate_jupiter_trade(mint, amount)
        if quote:
            log("Trade quote fetched. (Simulated)")
            spent += amount * 10
            time.sleep(5)
            log(f"Sell {mint} (simulated)")
            time.sleep(5)
    else:
        log("No new signals.")

    time.sleep(20)
