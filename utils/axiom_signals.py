
import requests

def fetch_trending_token():
    try:
        response = requests.get("https://api.axiom.xyz/trending")
        data = response.json()
        for token in data.get("results", []):
            if token.get("volume", 0) > 10000 and token.get("age", 0) < 86400:
                return token
    except Exception as e:
        print("[AXIOM] Error fetching signals:", e)
    return None
