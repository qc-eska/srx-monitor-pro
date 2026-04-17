import requests
from config import TELEGRAM_TOKEN, CHAT_ID, REQUEST_TIMEOUT

TOKEN = TELEGRAM_TOKEN

BASE_URL = f"https://api.telegram.org/bot{TOKEN}"


def send_message(text):
    if not TOKEN or not CHAT_ID:
        print("Missing TELEGRAM_TOKEN or CHAT_ID")
        return

    url = f"{BASE_URL}/sendMessage"

    try:
        response = requests.post(
            url,
            json={
                "chat_id": CHAT_ID,
                "text": text,
            },
            timeout=REQUEST_TIMEOUT,
        )
        response.raise_for_status()
    except requests.RequestException as exc:
        print(f"Telegram send failed: {exc}")
