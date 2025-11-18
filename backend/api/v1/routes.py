"""Route modules for API v1."""

from . import auth
from . import predictions
from . import charts
from . import transits
from . import health
from . import perplexity_endpoints
from . import knowledge
from . import consultant
from . import fortune
from . import personal_development
from . import synastry
from . import gemini_demo

__all__ = ["auth", "predictions", "charts", "transits", "health", "perplexity_endpoints", "knowledge", "consultant", "fortune", "personal_development", "synastry", "gemini_demo"]

# Import routers
auth_router = auth.router
predictions_router = predictions.router
charts_router = charts.router
transits_router = transits.router
health_router = health.router
perplexity_router = perplexity_endpoints.router
knowledge_router = knowledge.router
consultant_router = consultant.router
fortune_router = fortune.router
personal_development_router = personal_development.router
synastry_router = synastry.router
gemini_demo_router = gemini_demo.router
