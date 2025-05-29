
import os
import time
from utils.wallet import trade_from_wallet

def run_bot():
    print("[BOT] Running sniper bot with live trading...")
    smart_wallets = os.getenv("SMART_WALLETS_TO_ALWAYS_COPY", "").split(",")
    while True:
        for wallet in smart_wallets:
            wallet = wallet.strip()
            if wallet:
                trade_from_wallet(wallet)
        print("[BOT] Still running... monitoring trusted wallets.")
        time.sleep(60)
