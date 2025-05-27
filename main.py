import os
import time
import requests
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solana.rpc.api import Client
 

JUPITER_SWAP_API = "https://quote-api.jup.ag/v6/swap"
SOLANA_RPC = "https://api.mainnet-beta.solana.com"

PRIVATE_KEY = os.getenv("PRIVATE_KEY")
WALLET_ADDRESS = os.getenv("WALLET_ADDRESS")
DAILY_LIMIT = float(os.getenv("DAILY_LIMIT", "30"))
spent_today = 0

client = Client(SOLANA_RPC)

def log(msg):
    print(f"[BOT] {msg}", flush=True)

def get_swap_transaction(input_mint, output_mint, amount):
    try:
        response = requests.post(
            JUPITER_SWAP_API,
            json={
                "inputMint": input_mint,
                "outputMint": output_mint,
                "amount": int(amount * 1e9),
                "slippageBps": 100,
                "userPublicKey": WALLET_ADDRESS,
                "wrapUnwrapSOL": True,
                "dynamicComputeUnitLimit": True,
            },
        )
        return response.json()
    except Exception as e:
        log(f"Error fetching swap transaction: {e}")
        return None

def send_transaction(tx_base64):
    try:
        from solders.transaction import VersionedTransaction
        tx = VersionedTransaction.from_bytes(bytes.fromhex(tx_base64))
        res = client.send_raw_transaction(tx.serialize())
        log(f"Sent transaction: {res}")
        return res
    except Exception as e:
        log(f"Error sending transaction: {e}")
        return None

def fetch_trade_signal():
    # Placeholder for smart wallet signal
    return {"mint": "So11111111111111111111111111111111111111112", "amount": 0.01}

def execute_trade(trade_info):
    global spent_today
    mint = trade_info["mint"]
    amount = trade_info["amount"]
    tx_data = get_swap_transaction("So11111111111111111111111111111111111111112", mint, amount)
    if tx_data and "swapTransaction" in tx_data:
        raw_tx = tx_data["swapTransaction"]
        log("Fetched Jupiter swap transaction.")
        result = send_transaction(raw_tx)
        if result:
            spent_today += amount * 10
            log(f"Executed real BUY + SELL of {mint}")
    else:
        log("Trade failed or no transaction returned.")

log("REAL TRADING BOT ACTIVATED")

while True:
    if spent_today >= DAILY_LIMIT:
        log("Daily limit reached.")
        time.sleep(60)
        continue

    signal = fetch_trade_signal()
    if signal:
        execute_trade(signal)

    time.sleep(30)
