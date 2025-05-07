

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from backend.models import Alert
from backend.extension import dbs as db
from backend.app import app

def clear_alerts():
    with app.app_context():
        deleted = db.session.query(Alert).delete()
        db.session.commit()
        print(f"Deleted {deleted} alert(s).")

if __name__ == "__main__":
    clear_alerts()