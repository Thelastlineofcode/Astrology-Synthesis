"""Route modules for API v1."""

from . import auth
from . import predictions
from . import charts
from . import transits
from . import health

__all__ = ["auth", "predictions", "charts", "transits", "health"]

# Import routers
auth_router = auth.router
predictions_router = predictions.router
charts_router = charts.router
transits_router = transits.router
health_router = health.router
