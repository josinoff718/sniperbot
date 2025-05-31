import logging
import telebot
from config import TIER1_WALLETS, TIER2_WALLETS, TIER3_WALLETS, TELEGRAM_TOKEN

# Initialize bot with Telegram token
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(levelname)s] %(message)s')
logging.debug(f"Tier 1 wallets (no filters): {TIER1_WALLETS}")
logging.debug(f"Tier 2 wallets (basic filters): {TIER2_WALLETS}")
logging.debug(f"Tier 3 wallets (full filters): {TIER3_WALLETS}")

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

# (Keep your existing handlers and bot.polling() or equivalent below)
