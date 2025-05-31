import sqlite3

DB_PATH = "sniper.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Table for trade tracking
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS trades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            wallet TEXT,
            token TEXT,
            amount REAL,
            buy_price REAL,
            sell_price REAL,
            profit REAL,
            timestamp TEXT
        )
    """)

    # Table for wallet tracking
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tracked_wallets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            wallet_address TEXT NOT NULL,
            tier TEXT DEFAULT 'tier3'
        )
    """)

    conn.commit()
    conn.close()


def get_trade_count():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM trades")
    result = cursor.fetchone()[0]
    conn.close()
    return result

def get_total_profit():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(profit) FROM trades")
    result = cursor.fetchone()[0]
    conn.close()
    return result or 0.0

def get_tracked_wallets():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT wallet_address, tier FROM tracked_wallets")
    wallets = cursor.fetchall()
    conn.close()
    return wallets
 
