import sys
import types
import unittest
from unittest.mock import patch

dotenv_module = types.ModuleType("dotenv")
dotenv_module.load_dotenv = lambda: None
sys.modules.setdefault("dotenv", dotenv_module)

requests_module = types.ModuleType("requests")
requests_module.RequestException = Exception
requests_module.get = lambda *args, **kwargs: None
sys.modules.setdefault("requests", requests_module)

bs4_module = types.ModuleType("bs4")
bs4_module.BeautifulSoup = object
sys.modules.setdefault("bs4", bs4_module)

from core.analyzer import analyze_listings, scan_listings


class AnalyzeListingsTests(unittest.TestCase):
    @patch("core.analyzer.mark_seen")
    @patch("core.analyzer.is_seen", return_value=False)
    @patch("core.analyzer.fetch_listing_year", return_value=None)
    def test_srx_without_confirmed_year_is_skipped(self, _fetch_year, _is_seen, mark_seen):
        listings = [
            {
                "title": "Cadillac SRX 3.6 V6 AWD Elegance",
                "price": "48 600 PLN",
                "url": "https://www.otomoto.pl/osobowe/oferta/cadillac-srx-ID6HTCPD.html",
            }
        ]

        alerts = analyze_listings(listings)

        self.assertEqual(alerts, [])
        mark_seen.assert_not_called()

    @patch("core.analyzer.mark_seen")
    @patch("core.analyzer.is_seen", return_value=False)
    @patch("core.analyzer.fetch_listing_year", return_value=2008)
    def test_srx_first_gen_with_confirmed_year_is_allowed(self, _fetch_year, _is_seen, mark_seen):
        listings = [
            {
                "title": "Cadillac SRX 3.6 V6 AWD",
                "price": "29 900 PLN",
                "url": "https://example.com/srx-2008",
            }
        ]

        alerts = analyze_listings(listings)

        self.assertEqual(len(alerts), 1)
        self.assertIn("MATCH", alerts[0])
        mark_seen.assert_called_once_with("https://example.com/srx-2008")

    @patch("core.analyzer.mark_seen")
    @patch("core.analyzer.is_seen", return_value=True)
    @patch("core.analyzer.fetch_listing_year", return_value=2008)
    def test_scan_listings_counts_seen_matches_as_active(self, _fetch_year, _is_seen, mark_seen):
        listings = [
            {
                "title": "Cadillac SRX 3.6 V6 AWD",
                "price": "29 900 PLN",
                "url": "https://example.com/srx-2008?ref=abc",
            }
        ]

        result = scan_listings(listings)

        self.assertEqual(result["matching_count"], 1)
        self.assertEqual(result["new_alerts_count"], 0)
        self.assertEqual(result["alerts"], [])
        mark_seen.assert_not_called()


if __name__ == "__main__":
    unittest.main()
