
import os

def trade_from_wallet(wallet_address):
    proportion = float(os.getenv("COPY_TRADE_PROPORTION", 1.0))
    print(f"[BOT] Copying trade from wallet {wallet_address} with proportion {proportion}")
    if os.getenv("LIVE_TRADING_MODE", "off") == "on":
        print(f"[BOT] Executing real trade for {wallet_address}...")
    else:
        print(f"[BOT] Simulating trade for {wallet_address}...")
