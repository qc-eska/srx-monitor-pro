import requests
import os

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

BASE_URL = f"https://api.telegram.org/bot{TOKEN}"


def send_message(text):
    if not TOKEN or not CHAT_ID:
        print("Missing TELEGRAM_TOKEN or CHAT_ID")
        return

    url = f"{BASE_URL}/sendMessage"

    requests.post(url, json={
        "chat_id": CHAT_ID,
        "text": text
    })
