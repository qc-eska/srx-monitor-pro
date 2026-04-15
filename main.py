from scrapers.olx import fetch_olx
from scrapers.otomoto import fetch_otomoto
from core.analyzer import analyze_listings
from telegram.bot import send_alert
import time

def run():
    send_alert("🚗 SRX monitor uruchomiony (PRO 24/7)")

    while True:
        try:
            listings = []

            # pobieranie danych
            listings += fetch_olx()
            listings += fetch_otomoto()

            # analiza + alerty
            alerts = analyze_listings(listings)

            for alert in alerts:
                send_alert(alert)

            print(f"Scan done: {len(listings)} listings found")

        except Exception as e:
            print("ERROR:", e)
            send_alert(f"⚠️ Błąd systemu: {e}")

        time.sleep(1800)  # 30 minut

if __name__ == "__main__":
    run()
