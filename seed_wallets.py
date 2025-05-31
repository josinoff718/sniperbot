
import sqlite3

wallets = [
    ("yuYsfkt3qrUEapza7HEBnYW9A557pjVNsfrLGXLaN69", "tier1"),
    ("9Rqb3Nvru6Mjtnf8wWh9YFe5dqfeLbGXL6vCn8DdCvTg", "tier2"),
    ("BQ9BX1fnN2e2ByskRAybiw21MPtJLUpDY191Cgq3LyKp", "tier2"),
]

conn = sqlite3.connect("sniper.db")
cursor = conn.cursor()

for address, tier in wallets:
    cursor.execute("INSERT INTO tracked_wallets (wallet_address, tier) VALUES (?, ?)", (address, tier))

conn.commit()
conn.close()
print("✅ Wallets seeded.")
