"""
Authentication API endpoints - Production-ready auth system.
Includes registration, login, JWT refresh, user profile, and API key management.

This file simply re-exports the complete router from auth_endpoints.py
which contains all authentication logic and endpoints.
"""

from .auth_endpoints import router

__all__ = ["router"]

