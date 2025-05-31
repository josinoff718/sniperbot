import logging
import telebot
import re
from config import TIER1_WALLETS, TIER2_WALLETS, TIER3_WALLETS, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID

# Initialize bot with Telegram token
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(levelname)s] %(message)s')
logging.debug(f"Tier 1 wallets (no filters): {TIER1_WALLETS}")
logging.debug(f"Tier 2 wallets (basic filters): {TIER2_WALLETS}")
logging.debug(f"Tier 3 wallets (full filters): {TIER3_WALLETS}")

# Global variable for daily trade limit
daily_trade_limit = None

def send_telegram_message(text, chat_id=None):
    """
    Send a Telegram message to the specified chat_id, or to the owner if none provided.
    """
    target_id = chat_id if chat_id else TELEGRAM_CHAT_ID
    bot.send_message(target_id, text, parse_mode="Markdown")

def telegram_command_loop():
    """
    Start the Telegram bot polling loop to listen for commands and messages.
    """
    global daily_trade_limit
    # Initialize daily_trade_limit from config
    from config import DAILY_TRADE_LIMIT
    daily_trade_limit = DAILY_TRADE_LIMIT

    send_telegram_message("🚀 SniperBot is now online and listening for commands.")
    bot.polling(none_stop=True)

@bot.message_handler(commands=["wallets"])
def show_wallets(message):
    """
    Send a Telegram message listing wallets by tier.
    """
    text_lines = []

    # Tier 1
    text_lines.append("🏅 *Tier 1 (No Filters)*")
    if TIER1_WALLETS:
        for w in TIER1_WALLETS:
            text_lines.append(f"• {w}")
    else:
        text_lines.append("  (none)")

    # Tier 2
    text_lines.append("\n🐳 *Tier 2 (Basic Filters)*")
    if TIER2_WALLETS:
        for w in TIER2_WALLETS:
            text_lines.append(f"• {w}")
    else:
        text_lines.append("  (none)")

    # Tier 3
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
    """
    Adjust the daily trade limit. Usage: /limit <amount>
    """
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
    """
    Send a basic report: current daily limit and number of tracked wallets per tier.
    """
    global daily_trade_limit
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
