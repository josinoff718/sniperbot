import time
from sniper.wallets import get_tracked_wallets
from sniper.trading import execute_trade
from sniper.utils import send_telegram_message, get_daily_limit, get_wallet_tier

class SniperBot:
    def run(self):
        send_telegram_message("🧠 SniperBot is live and scanning wallets...")

        while True:
            wallets = get_tracked_wallets()
            for wallet in wallets:
                # Simulate trade detection
                token = "SOLANA_MEME"  # placeholder
                tier = get_wallet_tier(wallet)

                # Simulate decision
                if tier == 1:
                    execute_trade(token, amount_usd=10)
                    send_telegram_message(f"📥 Copied trade from {wallet} — Token: {token}")
                    
            time.sleep(10)  # prevent rate limit
 
