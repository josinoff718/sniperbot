import sqlite3

def init_db():
    conn = sqlite3.connect('trades.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS trades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            wallet TEXT,
            token TEXT,
            amount REAL,
            buy_price REAL,
            sell_price REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            status TEXT
        )
    ''')
    conn.commit()
    conn.close()
