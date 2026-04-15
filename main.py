from scrapers.olx import fetch_olx
from scrapers.otomoto import fetch_otomoto
from telegram.bot import send_alert
from core.analyzer import analyze_listings
import time

def run():
    while True:
        listings = []

        listings += fetch_olx()
        listings += fetch_otomoto()

        alerts = analyze_listings(listings)

        for alert in alerts:
            send_alert(alert)

        print("Scan done... waiting 30 min")
        time.sleep(1800)

if __name__ == "__main__":
    run()
