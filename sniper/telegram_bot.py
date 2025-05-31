import logging
import datetime
import csv
import os
import telebot

from config import (
    TIER1_WALLETS,
    TIER2_WALLETS,
    TIER3_WALLETS,
    TELEGRAM_TOKEN,
    TELEGRAM_CHAT_ID,
    DAILY_TRADE_LIMIT
)

from pnl_logger import append_pnl_record  # For logging trade P&L

# Initialize bot with Telegram token
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Configure logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s [%(levelname)s] %(message)s")
logging.debug(f"Tier 1 wallets (no filters): {TIER1_WALLETS}")
logging.debug(f"Tier 2 wallets (basic filters): {TIER2_WALLETS}")
logging.debug(f"Tier 3 wallets (full filters): {TIER3_WALLETS}")

# In-memory variable for the daily limit
daily_trade_limit = DAILY_TRADE_LIMIT

def send_telegram_message(text: str, chat_id: str = None):
    target_id = chat_id if chat_id else TELEGRAM_CHAT_ID
    bot.send_message(target_id, text, parse_mode="Markdown")

def telegram_command_loop():
    # Announce online
    send_telegram_message("🚀 SniperBot is now online and listening for commands.")
    bot.polling(none_stop=True)

@bot.message_handler(commands=["wallets"])
def show_wallets(message):
    text_lines = []
    text_lines.append("🏅 *Tier 1 (No Filters)*")
    if TIER1_WALLETS:
        for w in TIER1_WALLETS:
            text_lines.append(f"• {w}")
    else:
        text_lines.append("  (none)")

    text_lines.append("\n🐳 *Tier 2 (Basic Filters)*")
    if TIER2_WALLETS:
        for w in TIER2_WALLETS:
            text_lines.append(f"• {w}")
    else:
        text_lines.append("  (none)")

    text_lines.append("\n🔍 *Tier 3 (Full Filters)*")
    if TIER3_WALLETS:
        for w in TIER3_WALLETS:
            text_lines.append(f"• {w}")
    else:
        text_lines.append("  (none)")

    final_text = "\n".join(text_lines)
    bot.send_message(message.chat.id, final_text, parse_mode="Markdown")

@bot.message_handler(commands=["limit"])
def set_limit(message):
    global daily_trade_limit
    parts = message.text.strip().split()
    if len(parts) != 2 or not parts[1].isdigit():
        bot.send_message(message.chat.id, "Usage: /limit <amount> (e.g., /limit 300)")
        return
    new_limit = int(parts[1])
    daily_trade_limit = new_limit
    bot.send_message(message.chat.id, f"🔧 Daily trade limit set to ${daily_trade_limit}")

@bot.message_handler(commands=["report"])
def send_report(message):
    total_tier1 = len(TIER1_WALLETS)
    total_tier2 = len(TIER2_WALLETS)
    total_tier3 = len(TIER3_WALLETS)
    report_lines = [
        f"*Current Daily Trade Limit:* ${daily_trade_limit}",
        "",
        f"*Tier 1 wallets (no filters):* {total_tier1}",
        f"*Tier 2 wallets (basic filters):* {total_tier2}",
        f"*Tier 3 wallets (full filters):* {total_tier3}"
    ]
    report_text = "\n".join(report_lines)
    bot.send_message(message.chat.id, report_text, parse_mode="Markdown")

@bot.message_handler(commands=["daily_pnl"])
def handle_daily_pnl(message):
    csv_path = "daily_pnl.csv"
    if not os.path.exists(csv_path):
        bot.send_message(message.chat.id, "📊 Daily P&L: $0.00 (no records yet)")
        return

    today_utc = datetime.datetime.utcnow().date()
    yesterday_utc = today_utc - datetime.timedelta(days=1)
    target_date = yesterday_utc.strftime("%Y-%m-%d")

    total_pnl = 0.0
    trades_closed = 0

    with open(csv_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row["date"] == target_date:
                try:
                    pnl_value = float(row["pnl"])
                except ValueError:
                    continue
                total_pnl += pnl_value
                trades_closed += 1

    if trades_closed == 0:
        reply = f"📊 Daily P&L for {target_date}: $0.00 (no trades closed yesterday)"
    else:
        reply = (
            f"📊 Daily P&L for {target_date}:

"
            f"• Total P&L: ${total_pnl:.2f}
"
            f"• Trades closed: {trades_closed}"
        )

    bot.send_message(message.chat.id, reply, parse_mode="Markdown")
