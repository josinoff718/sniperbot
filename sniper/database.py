import sqlite3

def init_db():
    conn = sqlite3.connect("trades.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS trades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            token TEXT,
            buy_price REAL,
            sell_price REAL,
            profit REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()
