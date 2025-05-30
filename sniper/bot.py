import os
import logging
import time
from sniper.utils import (
    send_telegram_message,
    get_smart_wallets,
    monitor_wallets_and_trade,
    summarize_daily_pnl,
    handle_telegram_commands,
    paused,
    convert_usd_to_sol
)

class SniperBot:
    def __init__(self):
        self.wallets = get_smart_wallets()
        self.usd_cap = float(os.getenv("DAILY_USD_LIMIT", 30))
        self.daily_limit = convert_usd_to_sol(self.usd_cap)
        self.debug = os.getenv("DEBUG", "false").lower() == "true"
        self.interval = int(os.getenv("SCAN_INTERVAL", 10))

    def run(self):
        send_telegram_message(
            f"🤖 Bot started. Tracking {len(self.wallets)} wallets. Daily Limit: ${self.usd_cap} (~{self.daily_limit} SOL)"
        )
        while True:
            try:
                handle_telegram_commands()
                if not paused:
                    monitor_wallets_and_trade(self.wallets, self.daily_limit, self.debug)
                if int(time.time()) % 3600 < self.interval:
                    summarize_daily_pnl()
            except Exception as e:
                logging.error(f"Error in trade loop: {e}")
            time.sleep(self.interval)