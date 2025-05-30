import requests

BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
url = f"https://api.telegram.org/bot{BOT_TOKEN}/deleteWebhook"
r = requests.get(url)
print(r.json())
