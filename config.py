import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", "1800"))
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "15"))
SEEN_DB_PATH = os.getenv("SEEN_DB_PATH", "srx.db")
STATUS_INTERVAL_HOURS = int(os.getenv("STATUS_INTERVAL_HOURS", "4"))
STATUS_START_HOUR = int(os.getenv("STATUS_START_HOUR", "7"))
STATUS_END_HOUR = int(os.getenv("STATUS_END_HOUR", "23"))
APP_TIMEZONE = os.getenv("APP_TIMEZONE", "Europe/Warsaw")
