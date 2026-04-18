import sys
import types
import unittest
from unittest.mock import MagicMock, patch

dotenv_module = types.ModuleType("dotenv")
dotenv_module.load_dotenv = lambda: None
sys.modules["dotenv"] = dotenv_module


class FakeSession:
    def __init__(self, responses):
        self._responses = iter(responses)
        self.headers = {}

    def get(self, *args, **kwargs):
        response = next(self._responses)
        if isinstance(response, Exception):
            raise response
        return response


requests_module = types.ModuleType("requests")
requests_module.RequestException = Exception
requests_module.Session = lambda: FakeSession([])
sys.modules["requests"] = requests_module

bs4_module = types.ModuleType("bs4")
bs4_module.BeautifulSoup = object
sys.modules["bs4"] = bs4_module

from scrapers.autoplac import fetch_autoplac


class AutoplacTests(unittest.TestCase):
    @patch("scrapers.autoplac.BeautifulSoup")
    @patch("scrapers.autoplac.requests.Session")
    def test_fetch_autoplac_normalizes_urls_and_skips_duplicates(self, session_factory, soup_factory):
        homepage = MagicMock()
        homepage.raise_for_status.return_value = None

        listing_page = MagicMock()
        listing_page.raise_for_status.return_value = None
        listing_page.text = "<html></html>"

        session_factory.return_value = FakeSession(
            [homepage, listing_page, listing_page, listing_page]
        )

        first_link = MagicMock()
        first_link.get.side_effect = lambda key, default="": {
            "href": "/oferta/cadillac/srx/test-ogloszenie?utm=abc"
        }.get(key, default)
        first_link.get_text.return_value = "Cadillac SRX 3.6 V6"

        duplicate_link = MagicMock()
        duplicate_link.get.side_effect = lambda key, default="": {
            "href": "https://autoplac.pl/oferta/cadillac/srx/test-ogloszenie?foo=1"
        }.get(key, default)
        duplicate_link.get_text.return_value = "Cadillac SRX 3.6 V6"

        invalid_link = MagicMock()
        invalid_link.get.side_effect = lambda key, default="": {
            "href": "/kontakt"
        }.get(key, default)
        invalid_link.get_text.return_value = "Kontakt"

        soup = MagicMock()
        soup.select.return_value = [first_link, duplicate_link, invalid_link]
        soup_factory.return_value = soup

        listings = fetch_autoplac()

        self.assertEqual(
            listings,
            [
                {
                    "title": "Cadillac SRX 3.6 V6",
                    "price": "brak",
                    "url": "https://autoplac.pl/oferta/cadillac/srx/test-ogloszenie",
                }
            ],
        )


if __name__ == "__main__":
    unittest.main()
