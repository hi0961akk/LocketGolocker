"""
Public Blueprint - User-facing routes (no authentication).

Routes:
  GET  /              - Frontend homepage
  POST /api/get-user-info   - Preview user profile
  POST /api/restore         - Queue restore request
  POST /api/queue/status    - Poll request status
  GET  /api/queue/global-status - Aggregate queue stats
"""

from flask import Blueprint

bp = Blueprint('public', __name__)

# Import routes to register them with this blueprint
from . import routes  # noqa: F401, E402
