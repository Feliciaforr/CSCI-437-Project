import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from threading import Thread
from backend.alerts.alert_logic import start_alert_checks
from backend.app import app  #

if __name__ == "__main__": 
        print("Starting Alerts Runner...")
        start_alert_checks()