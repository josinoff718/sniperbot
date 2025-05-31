import sqlite3
from sniper.constants import SMART_WALLETS_TO_ALWAYS_COPY

def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS trades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        token TEXT,
        amount REAL,
        profit REAL
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS tracked_wallets (
        address TEXT PRIMARY KEY
    )''')
    conn.commit()
    conn.close()

def get_trade_count():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM trades")
    result = c.fetchone()[0]
    conn.close()
    return result

def get_total_profit():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT SUM(profit) FROM trades")
    result = c.fetchone()[0]
    conn.close()
    return result or 0

def get_tracked_wallets():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT address FROM tracked_wallets")
    result = [row[0] for row in c.fetchall()]
    conn.close()
    return result

def seed_wallets():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS tracked_wallets (address TEXT PRIMARY KEY)")
    for wallet in SMART_WALLETS_TO_ALWAYS_COPY:
        c.execute("INSERT OR IGNORE INTO tracked_wallets (address) VALUES (?)", (wallet,))
    conn.commit()
    conn.close()