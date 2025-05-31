import datetime
import os

CSV_PATH = "daily_pnl.csv"

def append_pnl_record(wallet: str, token: str, pnl: float):
    """
    Call this whenever your bot finishes a trade.
    It appends one line to daily_pnl.csv:
      YYYY-MM-DD,<wallet>,<token>,<pnl>
    """
    # 1) Get today’s date in UTC, e.g. "2025-05-31"
    today_date = datetime.datetime.utcnow().strftime("%Y-%m-%d")

    # 2) If the CSV file doesn’t exist yet, create it with the header line:
    if not os.path.exists(CSV_PATH):
        with open(CSV_PATH, "w", encoding="utf-8") as f:
            f.write("date,wallet,token,pnl\n")

    # 3) Append one new line at the end:
    with open(CSV_PATH, "a", encoding="utf-8") as f:
        # Example appended line: "2025-05-31,MyWallet123,SOL,12.34\n"
        f.write(f"{today_date},{wallet},{token},{pnl:.2f}\n")
