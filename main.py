from scrapers.olx import fetch_olx
from scrapers.otomoto import fetch_otomoto
from scrapers.autoplac import fetch_autoplac
from scrapers.sprzedajemy import fetch_sprzedajemy
from core.analyzer import analyze_listings
from telegram.bot import send_alert
import time

FIRST_RUN = True


def run():
    global FIRST_RUN

    send_alert("🚗 SRX monitor uruchomiony (PRO 24/7)")

    while True:
        try:
            listings = []

            listings += fetch_olx()
            listings += fetch_otomoto()
            listings += fetch_autoplac()
            listings += fetch_sprzedajemy()

            # 🧠 FIRST RUN = tylko zapis, bez alertów
            if FIRST_RUN:
                print(f"Bootstrap run: {len(listings)} listings saved, no alerts")
                FIRST_RUN = False
            else:
                alerts = analyze_listings(listings)

                for alert in alerts:
                    send_alert(alert)

            print(f"Scan done: {len(listings)} listings")

        except Exception as e:
            print("ERROR:", e)
            send_alert(f"⚠️ Błąd: {e}")

        time.sleep(1800)


if __name__ == "__main__":
    run()
