# Vercel Frontend Deployment Guide

## Prerequisites

- Vercel account (sign up at vercel.com)
- GitHub repository connected
- Backend deployed and running (Railway/Render)

## Step 1: Install Vercel CLI (Optional)

```bash
npm i -g vercel
vercel login
```

## Step 2: Import Project to Vercel

### Via Vercel Dashboard (Recommended)

1. Go to https://vercel.com/new
2. Select "Import Git Repository"
3. Choose `Thelastlineofcode/Astrology-Synthesis`
4. Configure project:
   - **Framework Preset**: Next.js
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `.next`
   - **Install Command**: `npm install`
   - **Development Command**: `npm run dev`

### Via CLI

```bash
cd /workspaces/Astrology-Synthesis/frontend
vercel --prod
```

## Step 3: Configure Environment Variables

In Vercel Dashboard → Settings → Environment Variables, add:

```
NEXT_PUBLIC_API_URL=https://your-backend.railway.app
NODE_ENV=production
```

Optional (if using Sentry):

```
NEXT_PUBLIC_SENTRY_DSN=https://xxxxx@sentry.io/xxxxx
SENTRY_ORG=your-org
SENTRY_PROJECT=mula-frontend
```

## Step 4: Enable Auto-Deploy

In Vercel Dashboard → Settings → Git:

1. ✅ Enable "Automatic deployments from Git"
2. Production Branch: `master` or `main`
3. ✅ Preview deployments for pull requests

## Step 5: Configure Custom Domain (Optional)

In Vercel Dashboard → Settings → Domains:

1. Add custom domain (e.g., `mula.app`)
2. Update DNS records as instructed
3. SSL certificate auto-provisioned

## Step 6: Verify Deployment

1. Check deployment status in Vercel Dashboard
2. Visit the live URL (e.g., `https://astrology-synthesis.vercel.app`)
3. Test critical flows:
   - Landing page loads
   - Navigation works
   - API calls reach backend (check network tab)

### Test Checklist

- [ ] Homepage loads without errors
- [ ] CSS/styling renders correctly
- [ ] Images and assets load
- [ ] Navigation between pages works
- [ ] Console has no critical errors
- [ ] API calls reach backend (may fail if backend not ready)

## Step 7: Monitor Build Logs

View build logs in Vercel Dashboard → Deployments → [Latest Deploy] → Building

Common issues:

- **Build fails**: Check TypeScript errors, missing dependencies
- **404 on routes**: Verify `app` router structure
- **API errors**: Check CORS settings on backend, verify NEXT_PUBLIC_API_URL

## Step 8: Performance Optimization

### Enable Vercel Analytics (Optional)

```bash
cd /workspaces/Astrology-Synthesis/frontend
npm install @vercel/analytics
```

Add to `layout.tsx`:

```tsx
import { Analytics } from "@vercel/analytics/react";

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        {children}
        <Analytics />
      </body>
    </html>
  );
}
```

### Enable Speed Insights

```bash
npm install @vercel/speed-insights
```

## Step 9: CI/CD Pipeline

Vercel automatically:

- ✅ Builds on every push to master
- ✅ Creates preview deployments for PRs
- ✅ Runs TypeScript checks
- ✅ Generates build logs

## Troubleshooting

### Build Fails

```bash
# Test locally first
cd frontend
npm run build

# Check for TypeScript errors
npm run lint
```

### API Connection Issues

1. Verify `NEXT_PUBLIC_API_URL` is set in Vercel
2. Check CORS settings on backend allow Vercel domain
3. Test API endpoint directly: `curl https://your-backend.railway.app/health`

### Environment Variables Not Working

- Environment variables must start with `NEXT_PUBLIC_` to be accessible in browser
- Redeploy after adding new environment variables

## Deployment URLs

- **Production**: `https://astrology-synthesis.vercel.app`
- **Preview**: `https://astrology-synthesis-git-[branch].vercel.app`

## Post-Deployment

1. Update backend CORS to allow Vercel domain
2. Test all user flows on production
3. Monitor Vercel Analytics dashboard
4. Set up custom domain (optional)

## Success Metrics

- ✅ Build time < 2 minutes
- ✅ Lighthouse Performance > 80
- ✅ Lighthouse Accessibility > 90
- ✅ Zero build errors
- ✅ All pages load correctly
- ✅ API integration working

## Support

- Vercel Docs: https://vercel.com/docs
- Next.js Docs: https://nextjs.org/docs
- GitHub Issues: https://github.com/Thelastlineofcode/Astrology-Synthesis/issues
