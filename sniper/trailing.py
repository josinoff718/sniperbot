import logging

class TradeTracker:
    def __init__(self, entry_price, take_profit=2.0, trailing_stop_pct=0.3):
        self.entry_price = entry_price
        self.take_profit_price = entry_price * take_profit
        self.trailing_stop_pct = trailing_stop_pct
        self.highest_price = entry_price
        self.active = True

    def update_price(self, current_price):
        if not self.active:
            return None

        if current_price > self.highest_price:
            self.highest_price = current_price

        stop_price = self.highest_price * (1 - self.trailing_stop_pct)

        if current_price < stop_price:
            self.active = False
            logging.info(f"Triggered trailing stop: peak {self.highest_price}, current {current_price}, stop {stop_price}")
            return "SELL"

        if current_price >= self.take_profit_price:
            logging.info(f"Target 2x profit hit: current {current_price}, entry {self.entry_price}")
            return "HOLD"

        return None