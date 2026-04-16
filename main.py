from scrapers.olx import fetch_olx
from scrapers.otomoto import fetch_otomoto
from scrapers.autoplac import fetch_autoplac
from scrapers.sprzedajemy import fetch_sprzedajemy
from core.analyzer import analyze_listings
from telegram.bot import send_message
from database.db import mark_seen
import time


def run():
    send_message("🚗 SRX monitor uruchomiony (PRO 24/7)")

    while True:
        try:
            listings = []

            listings += fetch_olx()
            listings += fetch_otomoto()
            listings += fetch_autoplac()
            listings += fetch_sprzedajemy()

            print("TOTAL:", len(listings))

            alerts = analyze_listings(listings)

            for alert in alerts:
                send_message(alert)

            print(f"Scan done: {len(listings)} listings")

        except Exception as e:
            print("ERROR:", e)
            send_message(f"⚠️ Błąd: {e}")

        time.sleep(1800)


if __name__ == "__main__":
    run()
