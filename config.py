DEBUG = True
TELEGRAM_CHAT_ID = "your_chat_id_here"
TELEGRAM_TOKEN   = "your_bot_token_here"
SIMULATION_MODE  = True

# ── Tier 1: No-filter wallets (your two always-track addresses) ──
TIER1_WALLETS = [
    "9Rqb3Nvru6Mjtnf8wWh9YFe5dqfeLbGXL6vCn8DdCvTg",
    "BQ9BX1fnN2e2ByskRAybiw21MPtJLUpDY191Cgq3LyKp",
]

# ── Tier 2: “Large whale” wallets (basic-filter tracking) ──
TIER2_WALLETS = [
    "A1b2C3D4E5f6G7H8I9J0K1L2M3N4O5P6Q7R8S9T0",
    "Z9Y8X7W6V5U4T3S2R1Q0P9O8N7M6L5K4J3I2H1G0",
]

# ── Tier 3: “Other vetted smart-money” wallets (full-filter tracking) ──
TIER3_WALLETS = [
    "F1e2D3c4B5a6Z7y8X9w8V7u6T5s4R3q2P1o0N9M8",
    "Y1x2W3v4U5t6S7r8Q9p8O7n6M5l4K3j2I1h0G9F8",
    "E1f2G3h4J5k6L7m8N9o8P7q6R5s4T3u2V1w0X9Y8",
]

# (Optional) Master list of all tracked wallets
TRUSTED_WALLETS = TIER1_WALLETS + TIER2_WALLETS + TIER3_WALLETS

DAILY_TRADE_LIMIT = 300
