from backend.alerts import alert_runner
import unittest
from unittest.mock import patch

class TestAlertRunner(unittest.TestCase):
    def test_alert_runner(self):
        with patch("backend.alerts.alert_runner.start_alert_checks") as mock_start_alert_checks, \
             patch("builtins.print") as mock_print:
            alert_runner.main()
            mock_print.assert_called_with("Starting Alerts Runner...")
            mock_start_alert_checks.assert_called_once()

if __name__ == '__main__':
    unittest.main()
