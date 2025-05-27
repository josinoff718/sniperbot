import os
import time
import requests
from solders.keypair import Keypair
from solana.rpc.api import Client
from solders.transaction import VersionedTransaction
from base64 import b64decode

JUPITER_QUOTE_URL = "https://quote-api.jup.ag/v6/swap"
RPC_URL = "https://api.mainnet-beta.solana.com"

PRIVATE_KEY = os.getenv("PRIVATE_KEY")
WALLET_ADDRESS = os.getenv("WALLET_ADDRESS")
DAILY_LIMIT = float(os.getenv("DAILY_LIMIT", "30"))

client = Client(RPC_URL)
spent_today = 0

# Sample wallets being monitored (real ones should be dynamically pulled or preloaded)
SMART_WALLETS = [
    "9Rqb3Nvru6Mjtnf8wWh9YFe5dqfeLbGXL6vCn8DdCvTg",
    "BQ9BX1fnN2e2ByskRAybiw21MPtJLUpDY191Cgq3LyKp"
]

def log(msg):
    print(f"[BOT] {msg}", flush=True)

def fetch_recent_tokens():
    try:
        response = requests.get("https://client-api.pump.fun/tokens/trending")
        tokens = response.json().get("tokens", [])
        return tokens
    except Exception as e:
        log(f"Error fetching tokens: {e}")
        return []

def filter_tokens(tokens):
    valid = []
    for t in tokens:
        if (
            t.get("holder_count", 0) > 1000
            and t.get("volume_24h", 0) > 5000
            and t.get("age_minutes", 9999) < 90
        ):
            valid.append(t)
    return valid

def get_trade_signal():
    tokens = fetch_recent_tokens()
    candidates = filter_tokens(tokens)
    for token in candidates:
        for whale in SMART_WALLETS:
            if whale in token.get("top_holders", []):
                return token.get("mint"), 0.01
    return None, None

def request_swap(input_mint, output_mint, amount):
    try:
        res = requests.post(JUPITER_QUOTE_URL, json={
            "inputMint": input_mint,
            "outputMint": output_mint,
            "amount": int(amount * 1e9),
            "slippageBps": 100,
            "userPublicKey": WALLET_ADDRESS,
            "wrapUnwrapSOL": True,
            "dynamicComputeUnitLimit": True,
        })
        data = res.json()
        return data.get("swapTransaction")
    except Exception as e:
        log(f"Swap request failed: {e}")
        return None

def send_transaction(base64_txn):
    try:
        raw_tx = b64decode(base64_txn)
        tx = VersionedTransaction.from_bytes(raw_tx)
        result = client.send_raw_transaction(tx)
        log(f"Sent transaction: {result}")
        return True
    except Exception as e:
        log(f"Transaction failed: {e}")
        return False

log(">>> LIVE SNIPER BOT: Tracking whales and trading in real-time")

while True:
    if spent_today >= DAILY_LIMIT:
        log("Daily SOL limit reached.")
        time.sleep(60)
        continue

    mint, amount = get_trade_signal()
    if mint:
        log(f"Detected smart wallet token: {mint}")
        tx = request_swap("So11111111111111111111111111111111111111112", mint, amount)
        if tx:
            success = send_transaction(tx)
            if success:
                spent_today += amount * 10
                log(f"TRADE COMPLETE for {mint} (amount {amount})")
        else:
            log("No transaction returned from Jupiter.")
    else:
        log("No valid signal.")

    time.sleep(30)
