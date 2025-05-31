import telebot
import os
from sniper.database import get_trade_count, get_total_profit, get_tracked_wallets

API_KEY = os.getenv("API_KEY")
bot = telebot.TeleBot(API_KEY)

@bot.message_handler(commands=['limit'])
def handle_limit(message):
    bot.send_message(message.chat.id, "💰 Daily limit is $30")

@bot.message_handler(commands=['report'])
def handle_report(message):
    try:
        count = get_trade_count()
        total_profit = get_total_profit()
        bot.send_message(message.chat.id, f"📊 Trades: {count}")
        bot.send_message(message.chat.id, f"💵 Total Profit: ${total_profit or 0:.2f}")
    except Exception as e:
        bot.send_message(message.chat.id, f"⚠️ Error generating report: {str(e)}")

@bot.message_handler(commands=['wallets'])
def handle_wallets(message):
    try:
        wallets = get_tracked_wallets()
        wallet_text = '\n'.join(wallets) if wallets else "No wallets are currently being tracked."
        bot.send_message(message.chat.id, f"👛 Tracked Wallets:\n{wallet_text}")
    except Exception as e:
        bot.send_message(message.chat.id, f"⚠️ Error fetching wallets: {str(e)}")

def telegram_command_loop():
    print("🤖 Bot started listening for commands...")
    bot.polling(none_stop=True, interval=1, timeout=20)

def send_telegram_message(text):
    bot.send_message(chat_id=os.getenv("TELEGRAM_CHAT_ID"), text=text)
