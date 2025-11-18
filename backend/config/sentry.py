"""
Sentry Error Tracking Configuration for FastAPI Backend
"""
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
import os


def init_sentry():
    """
    Initialize Sentry SDK for error tracking and performance monitoring.
    Only initializes if SENTRY_DSN is set in environment variables.
    """
    sentry_dsn = os.getenv("SENTRY_DSN")
    
    if not sentry_dsn:
        print("⚠️  SENTRY_DSN not set. Sentry error tracking disabled.")
        return
    
    environment = os.getenv("ENVIRONMENT", "production")
    
    # Configure Sentry
    sentry_sdk.init(
        dsn=sentry_dsn,
        environment=environment,
        
        # Performance Monitoring
        traces_sample_rate=0.1 if environment == "production" else 1.0,
        
        # Integrations
        integrations=[
            FastApiIntegration(),
            SqlalchemyIntegration(),
        ],
        
        # Debug mode
        debug=environment != "production",
        
        # Additional context
        send_default_pii=False,  # Don't send Personally Identifiable Information
        
        # Filter out sensitive data
        before_send=filter_sensitive_data,
    )
    
    print(f"✅ Sentry initialized for {environment} environment")


def filter_sensitive_data(event, hint):
    """
    Filter out sensitive data before sending to Sentry.
    """
    # Remove sensitive headers
    if event.get("request", {}).get("headers"):
        headers = event["request"]["headers"]
        sensitive_headers = ["authorization", "cookie", "x-api-key"]
        
        for header in sensitive_headers:
            headers.pop(header, None)
    
    # Remove password fields from request data
    if event.get("request", {}).get("data"):
        data = event["request"]["data"]
        if isinstance(data, dict):
            data.pop("password", None)
            data.pop("old_password", None)
            data.pop("new_password", None)
    
    return event


def capture_error(exception: Exception, context: dict = None):
    """
    Manually capture an exception with additional context.
    
    Args:
        exception: The exception to capture
        context: Additional context to attach to the error
    
    Example:
        try:
            risky_operation()
        except Exception as e:
            capture_error(e, {"user_id": user.id, "action": "create_chart"})
    """
    if context:
        with sentry_sdk.push_scope() as scope:
            for key, value in context.items():
                scope.set_context(key, value)
            sentry_sdk.capture_exception(exception)
    else:
        sentry_sdk.capture_exception(exception)


def capture_message(message: str, level: str = "info"):
    """
    Capture a custom message.
    
    Args:
        message: The message to capture
        level: Log level (debug, info, warning, error, fatal)
    """
    sentry_sdk.capture_message(message, level=level)
