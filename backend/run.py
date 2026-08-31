import sys
import os

# Ensure backend directory is on python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import create_app
from database import init_db
from seed_data import seed_database

if __name__ == "__main__":
    print("[INFO] Initializing database & seeding sample opportunities...")
    init_db()
    seed_database()
    app = create_app()
    print("[INFO] Starting Smart Internship & Job Finder Flask Server on http://127.0.0.1:5000")
    app.run(host="127.0.0.1", port=5000, debug=False)
