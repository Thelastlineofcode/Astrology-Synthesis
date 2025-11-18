// Sentry Server Configuration for Next.js Frontend
import * as Sentry from "@sentry/nextjs";

Sentry.init({
  dsn: process.env.SENTRY_DSN,

  // Environment
  environment: process.env.NODE_ENV || "development",

  // Performance Monitoring
  tracesSampleRate: process.env.NODE_ENV === "production" ? 0.1 : 1.0,

  // Debug mode (only in development)
  debug: process.env.NODE_ENV !== "production",

  // Filter out sensitive data
  beforeSend(event) {
    // Remove sensitive data from event
    if (event.request?.headers) {
      delete event.request.headers["authorization"];
      delete event.request.headers["cookie"];
    }
    return event;
  },
});
