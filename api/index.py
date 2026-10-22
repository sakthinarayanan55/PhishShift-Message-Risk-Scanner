"""
Vercel Serverless Function Entrypoint for PhishShift Message Risk Scanner.
Exposes the WSGI Flask application object `app` for Vercel Python Runtime.
"""
import sys
from pathlib import Path

# Add project root directory to sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

# Import the initialized Flask application
from web.app import app

# Vercel looks for the `app` WSGI callable
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
