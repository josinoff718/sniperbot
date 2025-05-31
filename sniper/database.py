import sqlite3

def init_db():
    conn = sqlite3.connect("trades.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS trades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            profit REAL
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

