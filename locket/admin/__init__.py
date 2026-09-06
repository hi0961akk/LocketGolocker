"""
Admin Blueprint - Protected routes for account/token management.

All routes in this blueprint require session authentication via @admin_required.
Routes return JSON for /admin/api/* and redirect for HTML routes.
"""

from flask import Blueprint

bp = Blueprint('admin', __name__, url_prefix='/admin')

# Import routes to register them with this blueprint
from . import auth  # noqa: F401, E402
from . import routes  # noqa: F401, E402
