import sqlite3

 def init_db():
    conn = sqlite3.connect("sniper.db")
    cursor = conn.cursor()

    # Trades table
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

    # Tracked wallets table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tracked_wallets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            wallet_address TEXT NOT NULL,
            tier TEXT DEFAULT 'tier3'
        )
    """)

    conn.commit()
    conn.close()

        )
    ''')
    conn.commit()
    conn.close()

def get_trade_count():
    conn = sqlite3.connect("trades.db")
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM trades")
    count = c.fetchone()[0]
    conn.close()
    return count

def get_total_profit():
    conn = sqlite3.connect("trades.db")
    c = conn.cursor()
    c.execute("SELECT SUM(profit) FROM trades")
    total = c.fetchone()[0]
    conn.close()
    return total

def get_tracked_wallets():
    import sqlite3
    conn = sqlite3.connect("sniper.db")
    cursor = conn.cursor()
    cursor.execute("SELECT wallet_address FROM wallets")
    rows = cursor.fetchall()
    conn.close()
    return [row[0] for row in rows]

import sqlite3

def get_tracked_wallets():
    conn = sqlite3.connect("sniper.db")
    cursor = conn.cursor()
    cursor.execute("SELECT wallet_address FROM tracked_wallets")
    rows = cursor.fetchall()
    conn.close()
    return [row[0] for row in rows]
