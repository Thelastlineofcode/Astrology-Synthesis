# HYBRID BUILD - LEAN SOLO BUDGET

## Real Numbers for One-Person Band

**Date**: November 4, 2025  
**Reality Check**: Solo founder, zero external funding  
**Strategy**: Bootstrap with cashflow, not capital

---

## 🎯 THE REAL QUESTION

> "Can I build this solo with no money?"

**Answer**: ✅ **YES. But strategy changes completely.**

The $40-50K budget assumed:

- Hired team (5-6 people)
- Infrastructure costs
- Marketing budget
- 8 weeks of runway

**You don't have that.** So we pivot to:

- Solo execution (you do everything)
- Zero-cost infrastructure (free tier + open source)
- Organic growth (no paid ads)
- Build → Launch → Revenue → Reinvest

---

## 💰 REALISTIC LEAN BUDGET

### Month 1 (Nov): Build Phase - $200-500

```
Domain + SSL:           $15 (yearly, ~$1.25/mo)
Vercel Pro (optional):  $20 (or use free tier)
Railway basic:          $0 (free tier includes plenty)
PostgreSQL:             $0 (Railway free tier)
Firebase:               $0 (free tier)
SendGrid:               $0 (free tier, 100 emails/day)
Stripe:                 $0 (3.5% commission on revenue)
GitHub:                 $0 (free)
Claude API:             $5-10 (testing, not production yet)
-------
TOTAL MONTH 1:          ~$40 actual cash

Hidden costs:
- Your time: Infinite (unpaid)
- Internet/laptop: Already have
- Coffee: On you
```

### Month 2-3 (Dec-Jan): Revenue Phase - $200-500/month

```
Same infrastructure:    $40/month
Scale Claude API:       $50-100 (if features use it heavily)
Possible Railway paid:  $0 (stay on free tier longer)
-------
TOTAL:                  ~$100-150/month

Offset by revenue:
- If you hit $300-500 MRR in Week 2
- Stripe takes 3.5% ($10-17)
- You keep $283-483
- Net positive by Week 2
```

### Months 4+ (Feb onwards): Sustainable - $0-200/month

```
All paid for by revenue
Reinvest profits into:
- Better hosting (if needed)
- Marketing (if wanted)
- Team hire (if successful)
```

---

## 🏗️ LEAN INFRASTRUCTURE (All Free/Nearly Free)

| Service              | Cost        | Alternative         | Notes                    |
| -------------------- | ----------- | ------------------- | ------------------------ |
| **Hosting Frontend** | $0          | Vercel free         | Auto-deploy from GitHub  |
| **Hosting Backend**  | $0          | Railway free tier   | 500 hours/month included |
| **Database**         | $0          | Railway free tier   | PostgreSQL included      |
| **Auth**             | $0          | JWT + NextAuth      | Open source, free        |
| **Payments**         | 3.5%        | Stripe              | Only pay on revenue      |
| **Email**            | $0          | SendGrid free       | 100/day free tier        |
| **Notifications**    | $0          | Firebase free       | Generous free tier       |
| **AI Integration**   | Pay-per-use | Claude API          | $0.003 per 1K tokens     |
| **Analytics**        | $0          | Plausible free tier | Or use Vercel Analytics  |
| **Monitoring**       | $0          | Sentry free tier    | Good enough for MVP      |
| **Domain**           | $10-15/yr   | Namecheap           | Split across months      |

**TOTAL MONTHLY: $0-50 for infrastructure** (until you scale)

---

## ⏰ REALISTIC SOLO TIMELINE

Original plan assumed 6 people × 8 weeks = parallel work

Solo reality: Sequential work, ~3x longer timeline

```
Week 1-3:   Setup + Auth + Birth Chart Form
Week 2-4:   Dasha Timer first version (basic)
Week 4-5:   Deploy + get feedback from beta users
Week 5-6:   Iterate on Dasha Timer based on feedback
Week 6-8:   Build Compatibility feature (reuse components)
Week 8-10:  Deploy Compatibility + social sharing
Week 10-12: Monetization setup (Stripe) + premium features
Week 12-16: Marketing push + user acquisition
Week 16+:   Stabilize, iterate, grow revenue

REALISTIC: 4 months (16 weeks) solo vs 8 weeks with team
```

---

## 🤔 THE HARD TRADE-OFFS

### With $40-50K (Team of 6)

✅ Fast (8 weeks)  
✅ Parallel work  
✅ Higher quality (specialized roles)  
❌ Expensive  
❌ Need external funding  
❌ Equity dilution (series A later)

### With $0 (Solo)

✅ No funding needed  
✅ 100% ownership  
✅ Revenue goes straight to you  
✅ Lean discipline (ruthless MVP)  
❌ Slower (4 months minimum)  
❌ You do everything  
❌ Sleep deprivation risk

---

## 💪 HOW SOLO ACTUALLY WORKS

### Month 1: Build (Nov 8 - Dec 6)

**Week 1-2**: Setup

- Next.js + FastAPI scaffold (using tutorials, templates)
- Local database
- Basic auth (NextAuth, JWT)
- Deploy to free tiers

**Week 3-4**: Dasha Timer MVP (minimal version)

- Birth chart form (simple)
- Dasha calculation API (reuse existing engine)
- Display current dasha
- Notifications via SendGrid (send email, no FCM)

**Week 5-6**: Deploy + Iterate

- Launch to 100 beta users (friends, Twitter followers)
- Get feedback
- Fix critical bugs
- Measure engagement

**Week 7-8**: Compatibility Feature

- Reuse components from Dasha Timer
- Add comparison logic
- Social sharing (Twitter, WhatsApp links)
- Simple share button (no complex analytics)

### Month 2: Monetize (Dec 6 - Jan 3)

**Week 9-10**: Stripe Setup

- One-click premium upgrade
- Simple paywall (report download)
- Email receipt

**Week 11-12**: Launch + Push

- ProductHunt
- Twitter threads
- Email list
- Reddit/Indie Hackers

**Week 13-16**: Iterate + Grow

- Based on revenue, iterate
- Add 1-2 more features if time
- Build audience
- Plan next phase

---

## 📊 SOLO SUCCESS METRICS (Different Targets)

### Month 1 Goal

- ✅ App deployed and working
- ✅ 50+ beta users
- ✅ 0 critical bugs
- ✅ Auth system solid
- ✅ You're sleeping sometimes

### Month 2 Goal

- ✅ 500+ total users
- ✅ Compatibility working
- ✅ Stripe transactions processed (1-2 test buys)
- ✅ Preparing launch

### Month 3 Goal

- ✅ 2000+ users
- ✅ $200-500 MRR (realistic for solo)
- ✅ 30%+ D7 retention
- ✅ You can afford coffee

### Month 4+ Goals

- ✅ 5000+ users
- ✅ $500-1000 MRR
- ✅ Enough to hire first contractor
- ✅ Thinking about Series A much later

---

## 🛠️ THE SOLO STACK (Minimal, Free)

```
Frontend:
├── Next.js (free, vercel hosting free)
├── React (free)
├── Tailwind CSS (free, CDN)
└── Shadcn/ui (copy-paste components, free)

Backend:
├── FastAPI (free, open source)
├── Python 3.11 (free)
└── Railway (free tier sufficient)

Database:
├── PostgreSQL (Railway free tier)
└── No need for Redis yet

Auth:
├── NextAuth.js (free, open source)
└── JWT tokens (free)

Payments:
├── Stripe (free until you make sales)
└── 3.5% commission (acceptable)

Communication:
├── SendGrid (100 emails/day free)
└── No Twilio, no expensive SMS

AI:
├── Claude API (pay-per-use)
├── Only in premium features first
└── Monitor costs carefully

Hosting:
├── Vercel (free for frontend)
└── Railway (free for backend)

Monitoring:
├── Sentry (free tier)
└── Vercel Analytics (built-in)
```

**Total first month infrastructure: $0-50**

---

## 📋 SOLO EXECUTION CHECKLIST

### Pre-Launch (Week 1-2)

- [ ] GitHub repos created (free)
- [ ] Next.js + FastAPI starter scaffolded
- [ ] Deployed to Vercel + Railway (free tiers)
- [ ] Basic auth working
- [ ] Database connected

### MVP Version 1 (Week 3-6)

- [ ] Dasha Timer feature complete (basic version)
- [ ] Birth chart form works
- [ ] Display current dasha
- [ ] Email notifications via SendGrid (free)
- [ ] Share button (to Twitter, WhatsApp)

### First Beta Launch (Week 6-7)

- [ ] Deploy to production
- [ ] Invite 50 beta users
- [ ] Get feedback
- [ ] Fix critical bugs only
- [ ] Document issues (don't scope creep)

### Monetization Setup (Week 8-9)

- [ ] Stripe account (free to create)
- [ ] Simple "Buy Report" for $3-5
- [ ] Test transaction with your own card
- [ ] Email receipt works
- [ ] Download/email report works

### Compatibility Feature (Week 9-10)

- [ ] Reuse auth + forms from Dasha Timer
- [ ] Add comparison logic
- [ ] Simpler than Week 1 because components exist
- [ ] Social sharing buttons
- [ ] Deploy to production

### Public Launch (Week 11-12)

- [ ] ProductHunt (free)
- [ ] Twitter threads (free, your audience)
- [ ] Email blast to beta users (free via SendGrid)
- [ ] Reddit/HN posts (free)
- [ ] Track first revenue

### Iterate (Week 13+)

- [ ] Based on revenue, decide what to build next
- [ ] If $200/month → Maybe hire contractor part-time
- [ ] If $1000/month → Full-time sustainable
- [ ] Keep costs lean, reinvest revenue

---

## ⚠️ SOLO REALITIES

### What's Hard

- Exhaustion (you're doing 6 people's jobs)
- Bugs take longer to fix (only one pair of hands)
- Testing is slower (no QA person)
- Marketing happens in evenings
- Decision paralysis on 100 small choices

### What's Actually Easier

- No communication overhead
- No meetings (work when you want)
- No stakeholder management
- Lean by default (no features you don't need)
- Full ownership of decisions

### Burnout Prevention

- 6 hours work max per day (not 16)
- 2 days off per week minimum
- Set launch dates (force shipping)
- Celebrate small wins
- Remember: This is a marathon, not a sprint

---

## 💡 REALISTIC SOLO PATH

### Month 1: Build

- Time investment: 60-80 hours (6-8 weeks part-time or 2-3 weeks full-time)
- Money investment: $0-50
- Outcome: Deployed MVP with 50+ beta users

### Month 2: Refine + Feature #2

- Time: 40-60 hours
- Money: $0-100 (Stripe fees from sales)
- Outcome: 500+ users, $200-500 MRR

### Month 3: Marketing

- Time: 60-80 hours (more marketing, less coding)
- Money: Self-funded (reinvest revenue)
- Outcome: 2000+ users, $500-1000 MRR

### Month 4+: Growth

- Hire contractor (first $500-1000/month)
- Add 1-2 more features
- Think about Series A funding (or skip it, stay independent)
- Scale to 10K+ users organically

---

## 🚀 YOUR ACTUAL BUDGET

### Startup Costs: $0-100

```
Domain (yearly):        $15
Optional Vercel Pro:    $0 (use free tier)
Claude API credits:     $0 (pay-per-use)
Miscellaneous:          $0-85
---------
TOTAL:                  $15-100
```

### Monthly Operating: $0-150

```
Domain (amortized):     $1.25
Infrastructure:         $0 (free tiers)
Claude API usage:       $50-100 (if heavy use)
Miscellaneous:          $0-50
---------
TOTAL:                  $50-150/month

But offset by Stripe fees on revenue:
If you make $300 MRR → Pay $10.50 to Stripe
Net cost: -$40 (revenue positive)
```

---

## 🎯 BOTTOM LINE

**You don't need $40-50K**

You need:

- Time (4 months, 200-300 hours)
- Discipline (MVP only, no scope creep)
- Grit (it's lonely and hard)
- Free infrastructure (Vercel, Railway, etc.)
- Pay-as-you-go for extras (Claude, Stripe)

**Expected cash outlay: $100-500 for 4 months**

**Likely revenue by Month 4: $500-2000 MRR**

**Return**: ∞ (everything is profit after that)

---

## 📌 REVISED EXECUTION PLAN

Want me to create a **lean solo version** of the hybrid build plan?

Same features, same timeline targets, but:

- Solo execution (you do everything)
- Zero funding assumption
- Weekly milestones (not daily standups with 6 people)
- Scrappier approach (templates, copy-paste, less perfect)

**Should I rebuild the timeline for solo?** Yes/No

---

**Reality check: This is totally doable solo with $0.**

It's just a different game than hiring a team.

Which path appeals to you more?
