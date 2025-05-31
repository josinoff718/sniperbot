import sqlite3

def init_db():
    conn = sqlite3.connect("sniper.db")
    cursor = conn.cursor()

    # Create trades table
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

    # Create tracked_wallets table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tracked_wallets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            wallet_address TEXT NOT NULL,
            tier TEXT DEFAULT 'tier3'
        )
    """)

    conn.commit()
    conn.close()

