# Monitoring & Error Tracking Setup Guide

## Overview

This guide covers setting up comprehensive monitoring for the Mula application:
- **Sentry**: Error tracking for frontend and backend
- **Vercel Analytics**: Frontend performance monitoring
- **Uptime Monitoring**: Service availability tracking

---

## Part 1: Sentry Error Tracking

### 1.1 Create Sentry Account

1. Go to https://sentry.io/signup
2. Create account (GitHub SSO recommended)
3. Create organization: `mula` or `roots-revealed`

### 1.2 Create Projects

#### Frontend Project
1. New Project → Platform: Next.js
2. Name: `mula-frontend`
3. Copy DSN: `https://xxxxx@sentry.io/xxxxx`

#### Backend Project
1. New Project → Platform: Python (FastAPI)
2. Name: `mula-backend`
3. Copy DSN: `https://xxxxx@sentry.io/xxxxx`

### 1.3 Install Sentry Packages

#### Frontend
```bash
cd /workspaces/Astrology-Synthesis/frontend
npm install --save @sentry/nextjs
```

#### Backend
```bash
cd /workspaces/Astrology-Synthesis/backend
pip install sentry-sdk
# Add to requirements.txt: sentry-sdk==1.40.0
```

### 1.4 Configure Sentry

#### Frontend Environment Variables

Add to Vercel Dashboard → Environment Variables:
```bash
NEXT_PUBLIC_SENTRY_DSN=https://xxxxx@sentry.io/frontend-project-id
SENTRY_DSN=https://xxxxx@sentry.io/frontend-project-id
SENTRY_ORG=your-org-slug
SENTRY_PROJECT=mula-frontend
```

#### Backend Environment Variables

Add to Railway Dashboard → Environment Variables:
```bash
SENTRY_DSN=https://xxxxx@sentry.io/backend-project-id
ENVIRONMENT=production
```

#### Local Development

Frontend `.env.local`:
```bash
NEXT_PUBLIC_SENTRY_DSN=https://xxxxx@sentry.io/frontend-project-id
```

Backend `.env`:
```bash
SENTRY_DSN=https://xxxxx@sentry.io/backend-project-id
```

### 1.5 Initialize Sentry in Backend

Update `backend/main.py`:

```python
from backend.config.sentry import init_sentry
from backend.middleware.performance import PerformanceMiddleware

# Initialize Sentry
init_sentry()

# Add performance middleware
app.add_middleware(PerformanceMiddleware, slow_threshold_seconds=1.0)
```

### 1.6 Test Sentry Integration

#### Test Frontend
Add a test route `frontend/src/app/test-error/page.tsx`:
```tsx
'use client';
export default function TestError() {
  return (
    <button onClick={() => {
      throw new Error('Test Sentry Error from Frontend');
    }}>
      Trigger Error
    </button>
  );
}
```

Visit `/test-error` and click button. Check Sentry dashboard for error.

#### Test Backend
```bash
curl https://your-backend.railway.app/test-error
```

Check Sentry dashboard for error.

### 1.7 Configure Alerts

In Sentry Dashboard → Alerts:

1. **Critical Errors Alert**
   - Condition: Error level = Error or higher
   - Action: Email + Slack notification
   - Frequency: Immediate

2. **Performance Degradation**
   - Condition: P95 response time > 2s
   - Action: Email notification
   - Frequency: Every 15 minutes

3. **High Error Rate**
   - Condition: Error rate > 5% in 5 minutes
   - Action: Email + Slack notification
   - Frequency: Immediate

---

## Part 2: Vercel Analytics

### 2.1 Enable Vercel Analytics

#### Install Package
```bash
cd /workspaces/Astrology-Synthesis/frontend
npm install @vercel/analytics
```

#### Update Layout

Edit `frontend/src/app/layout.tsx`:

```tsx
import { Analytics } from '@vercel/analytics/react';

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
        {children}
        <Analytics />
      </body>
    </html>
  );
}
```

### 2.2 Enable Speed Insights

```bash
npm install @vercel/speed-insights
```

Update layout:
```tsx
import { SpeedInsights } from '@vercel/speed-insights/next';

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
        {children}
        <Analytics />
        <SpeedInsights />
      </body>
    </html>
  );
}
```

### 2.3 Configure Web Vitals Monitoring

Create `frontend/src/lib/performance.ts`:

```typescript
import * as Sentry from '@sentry/nextjs';
import { getCLS, getFID, getFCP, getLCP, getTTFB } from 'web-vitals';

export function initPerformanceMonitoring() {
  getCLS((metric) => {
    Sentry.captureMessage('CLS', {
      level: 'info',
      tags: { metric: 'cls' },
      extra: { value: metric.value },
    });
  });

  getLCP((metric) => {
    Sentry.captureMessage('LCP', {
      level: 'info',
      tags: { metric: 'lcp' },
      extra: { value: metric.value },
    });
  });

  getFID((metric) => {
    Sentry.captureMessage('FID', {
      level: 'info',
      tags: { metric: 'fid' },
      extra: { value: metric.value },
    });
  });
}
```

Call in `_app.tsx` or `layout.tsx`:
```tsx
import { initPerformanceMonitoring } from '@/lib/performance';

useEffect(() => {
  initPerformanceMonitoring();
}, []);
```

---

## Part 3: Uptime Monitoring

### 3.1 Use Uptime Robot (Free)

1. Go to https://uptimerobot.com/signup
2. Create free account

### 3.2 Add Monitors

#### Frontend Monitor
- **Monitor Type**: HTTP(s)
- **URL**: `https://astrology-synthesis.vercel.app`
- **Name**: Mula Frontend
- **Monitoring Interval**: 5 minutes
- **Alert Contacts**: Your email

#### Backend Monitor
- **Monitor Type**: HTTP(s)
- **URL**: `https://your-backend.railway.app/health`
- **Name**: Mula Backend API
- **Monitoring Interval**: 5 minutes
- **Alert Contacts**: Your email

### 3.3 Configure Alerts

- **Down Alert**: Email immediately
- **Up Alert**: Email when back online
- **Status Page**: Create public status page (optional)

### 3.4 Alternative: Better Uptime

For more features:
1. Go to https://betteruptime.com
2. Create account (free tier available)
3. Add same monitors
4. Configure Slack/Discord webhooks

---

## Part 4: Slack Integration (Optional)

### 4.1 Create Slack Workspace

1. Go to https://slack.com/create
2. Create workspace: `mula-team`
3. Create channels: `#alerts`, `#deployments`, `#errors`

### 4.2 Integrate with Sentry

1. Sentry Dashboard → Settings → Integrations
2. Find Slack → Install
3. Authorize workspace
4. Configure alert rules to send to `#errors`

### 4.3 Integrate with Vercel

1. Vercel Dashboard → Settings → Integrations
2. Find Slack → Add
3. Select channels for deployment notifications

### 4.4 Integrate with Railway

1. Railway Dashboard → Settings → Integrations
2. Add Slack webhook
3. Send to `#deployments` channel

---

## Part 5: Dashboard Setup

### 5.1 Sentry Dashboard

Create custom dashboard with widgets:
- Error rate over time
- Top 10 errors by frequency
- Top 10 errors by impact (users affected)
- Performance metrics (P50, P95, P99 response times)
- Error distribution by browser/device
- Geographic error distribution

### 5.2 Vercel Analytics Dashboard

Monitor:
- Real user metrics (RUM)
- Page load times
- Web Vitals (LCP, FID, CLS, TTFB, FCP)
- Top pages by traffic
- Traffic sources
- Devices/browsers

### 5.3 Railway Metrics Dashboard

Monitor:
- CPU usage
- Memory usage
- Network I/O
- Active connections
- Request rate
- Error rate

---

## Part 6: Monitoring Metrics & SLAs

### Service Level Objectives (SLOs)

| Metric | Target | Alert Threshold |
|--------|--------|-----------------|
| Uptime | 99.5% | < 99.0% |
| Error Rate | < 1% | > 5% |
| API Response Time (P95) | < 500ms | > 2s |
| Frontend LCP | < 2.5s | > 4s |
| Frontend CLS | < 0.1 | > 0.25 |
| Database Query Time | < 100ms | > 500ms |

### Alert Thresholds

- **Critical**: Immediate notification (email + Slack)
  - Service down
  - Error rate > 10%
  - Database connection lost

- **High**: 5-minute notification
  - Error rate > 5%
  - Response time > 2s

- **Medium**: 15-minute notification
  - Error rate > 2%
  - Slow queries detected

---

## Part 7: Testing Monitoring Setup

### 7.1 Test Error Tracking

```bash
# Frontend
# Visit /test-error and click button

# Backend
curl https://your-backend.railway.app/test-error
```

Check Sentry dashboard for errors.

### 7.2 Test Performance Monitoring

```bash
# Trigger slow endpoint
curl https://your-backend.railway.app/api/v1/slow-test
```

Check Sentry for performance warning.

### 7.3 Test Uptime Alerts

1. Stop Railway service temporarily
2. Wait for uptime alert (5-10 minutes)
3. Restart service
4. Wait for recovery alert

---

## Part 8: Maintenance

### Daily Checks
- [ ] Review error dashboard
- [ ] Check uptime status
- [ ] Monitor resource usage

### Weekly Tasks
- [ ] Review performance trends
- [ ] Analyze top errors
- [ ] Update alert thresholds if needed

### Monthly Tasks
- [ ] Review SLO compliance
- [ ] Analyze user behavior patterns
- [ ] Optimize slow endpoints
- [ ] Update monitoring configuration

---

## Cost Estimation

### Free Tier
- **Sentry**: 5K errors/month free
- **Uptime Robot**: 50 monitors free
- **Vercel Analytics**: Included with Hobby plan
- **Total**: $0/month

### Production (Recommended)
- **Sentry Team**: $26/month (50K errors)
- **Better Uptime**: $18/month (unlimited monitors)
- **Vercel Analytics**: Included with Pro ($20/month)
- **Total**: ~$64/month

---

## Success Criteria

- [ ] Sentry capturing errors from frontend and backend
- [ ] Alerts configured and tested
- [ ] Uptime monitoring active
- [ ] Performance metrics tracked
- [ ] Dashboards accessible to team
- [ ] Slack notifications working (if configured)
- [ ] All services monitored
- [ ] Alert noise < 5 false positives/day

---

## Support

- Sentry Docs: https://docs.sentry.io
- Vercel Analytics: https://vercel.com/docs/analytics
- Uptime Robot: https://uptimerobot.com/help
- Web Vitals: https://web.dev/vitals
