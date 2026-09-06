"""
Locket Gold Premium Unlocker — Flask Web Application
=====================================================

Main entry point for the application. This file can be used for:
- Local development (Flask dev server)
- Production deployment (Vercel, Heroku, or traditional VPS)
- Gunicorn/WSGI servers (via app.py:app factory)

The actual app logic is in the locket package (locket/__init__.py).
This module simply imports and exposes the Flask app instance.

Usage:
  Local dev:    python app.py
  Gunicorn:     gunicorn -c gunicorn.conf.py app:app
  Vercel:       Automatically runs via vercel.json entry point
"""

import os
import sys

# Ensure the locket package is importable
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from locket import create_app

# Create the Flask app instance
app = create_app()


if __name__ == "__main__":
    # Local development server
    # - debug=True enables auto-reload and detailed error pages
    # - use_reloader=False prevents Flask from spawning duplicate QueueManager threads
    # - port=5001 can be overridden via PORT env var (used by Vercel)
    port = int(os.getenv("PORT", 5001))
    app.run(
        host="0.0.0.0",
        port=port,
        debug=True,
        use_reloader=False
    )
