"""
Vercel Serverless Function Handler
====================================

Entry point for Vercel deployments. This file is automatically invoked
by Vercel's Python runtime for all HTTP requests matching the routes
defined in vercel.json.

This is separate from app.py because:
- Vercel expects serverless functions in /api directory
- The function must export an ASGI/WSGI application
- Each deployment creates a new process, so global state matters
"""

import os
import sys

# Add repo root to path so locket imports work
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from locket import create_app

# Create the Flask app exactly once
app = create_app()
