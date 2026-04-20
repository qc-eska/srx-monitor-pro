import sys
import types
import unittest
from datetime import datetime
from unittest.mock import patch

dotenv_module = types.ModuleType("dotenv")
dotenv_module.load_dotenv = lambda: None
sys.modules.setdefault("dotenv", dotenv_module)

from core.status import build_status_message, get_status_slot, should_send_status


class StatusTests(unittest.TestCase):
    def test_status_slot_matches_four_hour_windows(self):
        now = datetime(2026, 4, 20, 15, 30)
        self.assertEqual(get_status_slot(now), "2026-04-20:15")

    def test_status_slot_is_disabled_outside_hours(self):
        now = datetime(2026, 4, 20, 6, 59)
        self.assertIsNone(get_status_slot(now))

    @patch("core.status.get_meta", return_value="2026-04-20:11")
    def test_should_send_status_is_false_for_already_sent_slot(self, _get_meta):
        now = datetime(2026, 4, 20, 11, 30)
        self.assertFalse(should_send_status(now))

    @patch("core.status.get_meta", return_value="2026-04-20:11")
    def test_should_send_status_is_true_for_new_slot(self, _get_meta):
        now = datetime(2026, 4, 20, 15, 5)
        self.assertTrue(should_send_status(now))

    def test_build_status_message_contains_active_matches(self):
        now = datetime(2026, 4, 20, 19, 0)
        message = build_status_message(7, 42, 1, now)
        self.assertIn("Aktywnych ofert spełniających kryteria: 7", message)
        self.assertIn("Przeskanowanych w ostatnim cyklu: 42", message)
        self.assertIn("Nowych alertów w ostatnim cyklu: 1", message)


if __name__ == "__main__":
    unittest.main()
