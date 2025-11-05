# MULA MVP APP HOOKS — RAPID VALIDATION BRAINSTORM

## Simple, Expandable Ideas for 2-Week Sprint Launch

**Prepared:** November 4, 2025  
**Status:** Ready for Developer Handoff  
**Audience:** Founder, Developer, Growth Team

---

## 🎯 CRITICAL UPDATE - NOVEMBER 4, 2025

### What's Changed (Week 1 Complete)

✅ **Transit Analysis Bug - FIXED**

- All 4-system prediction integration now working
- Phase 3 no longer blocked
- Full syncretic synthesis operational

✅ **Recommended Strategy - REVISED**
The original MVP hooks plan proposed building 5 standalone features in isolation. **We now recommend building an integrated platform** that leverages the fixed Mula backend:

```
Original Approach: 5 separate apps (10-15 weeks, duplicated effort)
Recommended Approach: 1 integrated MVP platform (4 weeks, 50% faster, 2-3x better revenue)
```

**See:** `MVP_HOOKS_STRATEGIC_ALIGNMENT.md` for the detailed revised strategy.

### Key Improvements

| Aspect                   | Original        | Revised          |
| ------------------------ | --------------- | ---------------- |
| Build Timeline           | 10-15 weeks     | 4 weeks          |
| Estimated MRR            | $1.5K-3K        | $4K-9K           |
| Platform Integration     | None (isolated) | Full integration |
| Foundation for $100M ARR | No              | Yes              |
| Backend Reuse            | Duplicated      | Shared (80%+)    |

### Next Steps

1. **Review:** `MVP_HOOKS_STRATEGIC_ALIGNMENT.md` (complete strategy document)
2. **Decide:** Proceed with integrated MVP vs original isolated approach
3. **Plan:** 4-week development sprint (vs 10-15 weeks)
4. **Execute:** Week 2 infrastructure work begins immediately

---

## EXECUTIVE SUMMARY

Build ONE simple, high-value feature first (2-4 week sprint), validate with real users, then expand into the full Mula platform. Each idea below is:

- **Buildable in 2 weeks** with existing Mula tech
- **Monetizable from day 1** (freemium + premium upsell)
- **Socially shareable** (viral growth potential)
- **Expandable into full platform** (foundation for future features)

---

## 5 APP HOOK IDEAS (Ranked by Speed & Viral Potential)

---

## IDEA #1: "Daily Dasha Timer" ⏰ [RECOMMENDED FIRST BUILD]

### Overview

Push notification app that tells users exactly what planetary period they're in TODAY, plus one actionable recommendation based on that dasha.

### Core User Flow

1. User enters birth data (date, time, location)
2. App calculates their current Vimshottari Dasha (major, minor, sub-period)
3. Daily 8 AM push: "You're in Venus-Moon-Saturn until Nov 15. TODAY: Focus on creative partnerships, avoid confrontation."
4. User can tap → see full timing breakdown
5. Premium upsell: Hourly planetary updates ($9.99/mo)

### Why Build This First

- ✅ **Existing tech:** Vimshottari Dasha engine already built in Mula
- ✅ **Unique:** No competitor offers this specific timing focus
- ✅ **Daily habit:** People check like weather app (high retention)
- ✅ **Natural premium:** Hourly updates = obvious upsell
- ✅ **Foundational:** Base for full prediction engine

### Build Timeline

| Phase              | Duration      | Tasks                                                               |
| ------------------ | ------------- | ------------------------------------------------------------------- |
| **Design & Specs** | 2 days        | UI wireframes, API contract, notification templates                 |
| **Backend**        | 5 days        | Dasha calculation API, database (Supabase), push notification setup |
| **Frontend**       | 5 days        | Birth data form, timer display, sharing cards                       |
| **Payments & QA**  | 4 days        | Stripe integration, TestFlight, bug fixes                           |
| **TOTAL**          | **2-3 weeks** | MVP ready for launch                                                |

### Tech Stack

```
Frontend: Next.js 16 (mobile-responsive web app)
Backend: Supabase (Postgres database, auth)
Dasha Calculation: Leverage existing Mula engine
Push Notifications: Firebase Cloud Messaging or OneSignal (free tier)
Payments: Stripe (freemium model)
Hosting: Vercel (auto-deploy)
Analytics: Plausible (privacy-first)
```

### Monetization

| Tier        | Price     | Features                                      |
| ----------- | --------- | --------------------------------------------- |
| **Free**    | Free      | 1 daily dasha notification                    |
| **Pro**     | $9.99/mo  | Hourly updates, weekly forecast, remedies     |
| **Premium** | $24.99/mo | Unlimited updates + full birth chart analysis |

### Key Features

- **Daily notification** with one-line action
- **Timing breakdown** (show exactly when next period changes)
- **Shareable card** ("My dasha today is...")
- **Remedy recommendation** (link to Mula e-commerce)
- **Weekly forecast** view (what's coming)
- **Multiple chart types** (Sun, Moon, Ascendant dasha options)

### API Contracts (Draft)

**POST /api/user/birth-data**

```json
Request: { birthDate, birthTime, location, timezone }
Response: { userId, charts: { sun, moon, ascendant, natal } }
```

**GET /api/dasha/current**

```json
Request: { userId, chartType }
Response: {
  majorPeriod: "Venus (2023-2043)",
  minorPeriod: "Moon (2024-2026)",
  subPeriod: "Saturn (2025-2027)",
  todayFocus: "Creative partnerships",
  nextChange: "2025-11-15"
}
```

**POST /api/notifications/schedule**

```json
Request: { userId, frequency: "daily" }
Response: { scheduledAt: "08:00 EST", nextNotification: "2025-11-05" }
```

### Marketing & Viral Loop

- **Share button:** "My dasha today is Venus-Moon-Saturn 🪐" → TikTok, Instagram, Twitter
- **Hashtag:** #MyDashaToday (track trending periods)
- **Friend invite:** "Check your dasha" link (referral bonus if they subscribe)
- **Social media asset:** Beautiful dasha card template

### Success Metrics (Week 2 Launch)

- **100+ signups** = Product-market fit validated
- **10+ paid subscriptions** = People willing to pay
- **5+ social shares** = Viral potential
- **30%+ D7 retention** = Daily habit forming

### File Structure (Developer Handoff)

```
/src
  /api
    /dasha
      current.ts (GET /api/dasha/current)
      schedule.ts (POST /api/notifications/schedule)
    /user
      birth-data.ts (POST /api/user/birth-data)
  /components
    BirthDataForm.tsx
    DashaTimer.tsx (main display)
    DashaCard.tsx (shareable)
    TimingBreakdown.tsx
    RibbonBanner.tsx (next change countdown)
  /services
    dashaEngine.ts (leverage existing Mula calculation)
    notificationQueue.ts (Firebase/OneSignal)
  /pages
    index.tsx (landing)
    app.tsx (authenticated app)
    pricing.tsx (plans)
```

### Next Steps Post-Launch

1. Add multiple dasha types (Chara, Nakshatra)
2. Integrate remedy recommendations (e-commerce)
3. Add weekly forecasts + transit alerts
4. Cross-sell other hooks (compatibility, moon phases)

---

## IDEA #2: "Cosmic Compatibility Checker" 💕

### Overview

Instant synastry calculator: enter two birth charts, get compatibility score + one-line summary. Impulse purchase at $4.99 per report.

### Core User Flow

1. User inputs: "My birth" (or uses saved profile)
2. User inputs: "Their birth" (search by name or manual entry)
3. App calculates: Synastry aspects, Venus/Mars compatibility, relationship dynamics
4. Display: Score (0-100) + "Your compatibility with [Name]" + top 3 insights
5. Premium: Full report ($4.99 one-time) OR unlimited checks ($9.99/mo)

### Why Build This

- ✅ **Highly shareable:** People LOVE relationship content
- ✅ **Network effects:** Check with friends, partners, crushes
- ✅ **Impulse purchase:** $5 feels like nothing for insight
- ✅ **Massive TAM:** Everyone curious about compatibility
- ✅ **Quick monetization:** First feature to generate revenue

### Build Timeline

| Phase              | Duration      | Tasks                                          |
| ------------------ | ------------- | ---------------------------------------------- |
| **Design & Specs** | 2 days        | UI, scoring algorithm, result templates        |
| **Backend**        | 5 days        | Synastry calculation, aspect matching, scoring |
| **Frontend**       | 5 days        | Input form, results display, sharing cards     |
| **Payments & QA**  | 3 days        | Stripe one-time payment, TestFlight            |
| **TOTAL**          | **2-3 weeks** | MVP ready                                      |

### Tech Stack

```
Frontend: Next.js 16 SPA
Backend: Supabase + Node API
Synastry Calculation: Mula KP engine (existing)
Payments: Stripe (one-time purchase via webhook)
Hosting: Vercel
```

### Monetization

| Tier             | Price    | Features                                  |
| ---------------- | -------- | ----------------------------------------- |
| **Free Preview** | Free     | Score only (0-100)                        |
| **Full Report**  | $4.99    | Score + top 3 insights + chart comparison |
| **Unlimited**    | $9.99/mo | Check unlimited people, full history      |

### Key Features

- **Quick compatibility score** (instant gratification)
- **Shareable result card** (beautiful, social-friendly design)
- **Top 3 compatibility insights** (Venus, Mars, Moon)
- **Relationship advice** ("Best time to talk about future: Mars transit Nov 20")
- **Search other users** (if public profiles enabled)
- **History tracking** (premium: see all past checks)

### API Contracts

```json
POST /api/compatibility/check
Request: { user1ChartId, user2ChartId (or birth data) }
Response: {
  score: 78,
  summary: "Complementary fire-earth pairing",
  insights: [
    "Venus harmony: Strong romantic connection",
    "Mars challenge: Need communication around intensity",
    "Moon comfort: Emotional stability"
  ],
  bestTiming: "Nov 20-25 for deep conversations"
}
```

### Marketing Viral Loop

- **Share on socials:** "Me & [friend] are 78% compatible 💕" → Tag them
- **Hashtag:** #CosmicCompatibility
- **Challenge:** "Check compatibility with your crush" (TikTok trend)
- **Invite referral:** Friends who sign up get one free check

### Success Metrics (Week 2)

- **200+ signups** = High viral potential
- **30+ paid purchases** = Strong monetization
- **10+ shares** = Social validation
- **3x ROI on first paid users** = Sustainable model

### File Structure

```
/src
  /api
    /compatibility
      check.ts
      save.ts (premium history)
  /components
    CompatibilityForm.tsx
    ResultCard.tsx (shareable)
    InsightBreakdown.tsx
    ShareButtons.tsx
  /pages
    /app (authenticated)
    /checkout (payment)
    /history (premium feature)
```

### Expansion Path

- Team compatibility (3+ people)
- Friend group dynamics
- **B2B:** Corporate team building
- Integration with dating apps
- Full relationship timing guidance

---

## IDEA #3: "Moon Phase Rituals" 🌙

### Overview

Simple lunar calendar with daily ritual recommendations. Perfect for daily engagement + e-commerce integration.

### Core User Flow

1. User opens app → sees current moon phase
2. Daily ritual card: "New Moon in Scorpio: Set intentions for transformation. Light a black candle. ✨"
3. Calendar view: See all moon phases for the month
4. E-commerce: "Buy ritual kit" → links to dropship store
5. Premium: Custom rituals + alerts ($2.99/mo)

### Why Build This

- ✅ **Universal appeal:** Moon phases work for everyone (no birth chart needed)
- ✅ **Low friction:** Simple, beautiful, no complex calculations
- ✅ **E-commerce natural fit:** Ritual products = high margin
- ✅ **Evergreen content:** Moon cycles repeat yearly, reusable
- ✅ **Daily engagement:** People check moon phase frequently

### Build Timeline

| Phase                      | Duration      | Tasks                                     |
| -------------------------- | ------------- | ----------------------------------------- |
| **Design & Specs**         | 2 days        | Moon phase calendar UI, ritual database   |
| **Backend**                | 4 days        | Moon phase API, ritual content management |
| **Frontend**               | 4 days        | Calendar, ritual cards, shareable images  |
| **E-commerce Integration** | 3 days        | Shopify links, affiliate tracking         |
| **TOTAL**                  | **1-2 weeks** | MVP ready (fastest to launch)             |

### Tech Stack

```
Frontend: Next.js 16
Backend: Supabase
Moon Data: Skyfield library (Python backend) or lunar API
E-commerce: Shopify dropship links (affiliate tracking)
Hosting: Vercel
```

### Monetization

| Tier           | Price    | Features                                                |
| -------------- | -------- | ------------------------------------------------------- |
| **Free**       | Free     | Current moon phase + daily ritual                       |
| **Pro**        | $2.99/mo | Monthly calendar + weekly lunar alerts + ritual archive |
| **E-commerce** | Variable | Ritual kits, candles, crystals (dropship margin)        |

### Key Features

- **Current moon phase** (large, beautiful display)
- **Today's ritual** (one clear action + intention)
- **Monthly calendar** (all 8 moon phases highlighted)
- **Lunar alerts** (push notification 24hr before phase change)
- **Ritual archive** (save favorites, create custom)
- **E-commerce integration** (link to ritual product kits)
- **Shareability** (beautiful ritual cards for social)

### Content Strategy (Ritual Examples)

```
New Moon: "Set intentions for new beginnings"
Waxing Crescent: "Take action on your goals"
First Quarter: "Overcome challenges with determination"
Waxing Gibbous: "Refine and perfect your plans"
Full Moon: "Celebrate completion and gratitude"
Waning Gibbous: "Release what no longer serves"
Last Quarter: "Reflect and learn lessons"
Waning Crescent: "Rest and recharge"
```

### API Contracts

```json
GET /api/moon/current
Response: {
  phase: "Waxing Crescent",
  illumination: 0.23,
  zodiacSign: "Scorpio",
  nextPhase: "2025-11-10",
  daysUntil: 4
}

GET /api/rituals/today
Response: {
  ritual: "Set intentions for transformation",
  element: "Water",
  color: "Black",
  action: "Light a black candle, write your intentions",
  affirmation: "I am powerful and transforming",
  productLinks: [{ product: "Black Ritual Candle", url: "..." }]
}
```

### Marketing Viral Loop

- **Share ritual:** "Today's moon ritual: Set intentions 🌙" → TikTok, Instagram
- **Hashtag:** #MoonRitual #LunarLiving
- **Challenge:** "Moon phase challenge" (do the ritual for 29 days)
- **E-commerce tie-in:** "Get your ritual kit" → Shopify

### Success Metrics (Week 2)

- **300+ signups** = High appeal (no friction)
- **50+ ritual kit purchases** = E-commerce validation
- **8+ daily ritual shares** = Viral potential
- **40%+ D7 retention** = Daily habit

### File Structure

```
/src
  /api
    /moon
      current.ts
      calendar.ts (full month)
    /rituals
      today.ts
      archive.ts
  /components
    MoonDisplay.tsx (large, beautiful)
    RitualCard.tsx (shareable)
    MonthlyCalendar.tsx
    ProductLinks.tsx
  /pages
    /calendar
    /rituals
```

### Expansion Path

- Planetary rituals (Mars energy days, Venus days, etc.)
- Astrological year calendar (seasonal rituals)
- Personal birth chart rituals (aligned to your chart)
- Full timing system integration

---

## IDEA #4: "Remedy of the Day" 💎

### Overview

TikTok-style short-form app recommending ONE spiritual remedy daily based on transits + user's chart.

### Core User Flow

1. User enters: Sun, Moon, or Ascendant sign
2. App shows: "Today's remedy: Wear green, light sandalwood incense, work on throat chakra"
3. Beautiful card with imagery, emoji, colors
4. Tap to share → TikTok, Instagram, Twitter
5. "Buy remedy" button → Shopify dropship store

### Why Build This

- ✅ **Visual-first:** Perfect for TikTok/Instagram reposting
- ✅ **Action-oriented:** Gives people something to DO today
- ✅ **E-commerce hook:** Drives revenue immediately
- ✅ **Low barrier:** No full chart needed (just 1 input)
- ✅ **Daily engagement:** New remedy every day

### Build Timeline

| Phase              | Duration    | Tasks                                     |
| ------------------ | ----------- | ----------------------------------------- |
| **Design & Specs** | 2 days      | Card design templates, remedy database    |
| **Backend**        | 4 days      | Remedy engine, transit-based selection    |
| **Frontend**       | 4 days      | Sign input, remedy display, sharing cards |
| **E-commerce**     | 2 days      | Shopify integration, affiliate links      |
| **TOTAL**          | **2 weeks** | MVP ready                                 |

### Tech Stack

```
Frontend: Next.js 16
Backend: Supabase
Remedy Selection: AI-powered based on transits (Claude)
Image Generation: OG image API for sharing
Shopify: Dropship links with affiliate tracking
```

### Monetization

| Model          | Price         | Features                                     |
| -------------- | ------------- | -------------------------------------------- |
| **Free**       | Free          | 1 remedy/day, view only                      |
| **Pro**        | $4.99/mo      | Unlimited remedies, notifications, favorites |
| **E-commerce** | 50-70% margin | Dropship remedy products                     |

### Key Features

- **Daily remedy card** (visually beautiful)
- **Color coded** (chakra alignment, planetary energy)
- **Action list** (3-5 concrete steps)
- **Shareable image** (auto-generated for socials)
- **Product recommendation** ("Buy this crystal" → Shopify)
- **Remedy archive** (save favorites)
- **Push notifications** (daily remedy alert)

### Remedy Database (Examples)

```json
{
  "date": "2025-11-05",
  "remedy": "Amplify your voice",
  "color": "Green",
  "chakra": "Throat",
  "action": [
    "Wear green or blue clothing",
    "Light sandalwood incense",
    "Speak your truth for 10 minutes",
    "Drink green tea with intention"
  ],
  "affirmation": "My voice matters and is heard",
  "product_links": [
    { "name": "Green Aventurine Crystal", "shopify_link": "..." },
    { "name": "Sandalwood Incense Bundle", "shopify_link": "..." }
  ],
  "transit_reason": "Mercury in Gemini (communication day)"
}
```

### Marketing Viral Loop

- **Share remedy card:** "Today's remedy: Amplify your voice 💚" → TikTok
- **Hashtag:** #RemedyOfTheDay #SpiritualDaily
- **Challenge:** "30-day remedy challenge" (do daily remedy for a month)
- **Product integration:** "Get the remedy kit" → Shopify

### Success Metrics (Week 2)

- **200+ signups** = Good traction
- **15+ remedy purchases** = E-commerce works
- **10+ shares/day** = Social proof
- **35%+ D7 retention** = Habit forming

### File Structure

```
/src
  /api
    /remedy
      today.ts
      archive.ts
      recommend.ts (AI-powered)
  /components
    RemedyCard.tsx (main display)
    ShareCard.tsx (social sharing)
    ActionList.tsx
    ProductCarousel.tsx
  /pages
    /remedy
    /favorites
```

### Expansion Path

- Weekly remedies (deeper work)
- Multi-tradition remedies (Vedic, Vodou, Rosicrucian)
- Personal chart remedies (aligned to natal chart)
- Full subscription remedies club

---

## IDEA #5: "AI Oracle Chat" 🤖

### Overview

ChatGPT-style interface where users ask spiritual questions and get Mula-branded AI guidance based on timing and knowledge base.

### Core User Flow

1. User asks: "Should I take this job?"
2. App sends to Claude + Mula knowledge base
3. Response: Timing-based guidance + practical insight
4. Free: 3 questions/day, Premium: Unlimited ($9.99/mo)

### Why Build This

- ✅ **Immediate utility:** People have questions NOW
- ✅ **Habit-forming:** Like talking to a spiritual advisor
- ✅ **Low friction:** No birth chart needed initially
- ✅ **High perceived value:** $10/mo feels cheap vs $100/hr astrologer
- ✅ **Scalable:** Claude handles unlimited conversations

### Build Timeline

| Phase              | Duration      | Tasks                                              |
| ------------------ | ------------- | -------------------------------------------------- |
| **Design & Specs** | 2 days        | Chat UI, prompt engineering                        |
| **Backend**        | 5 days        | Claude integration, rate limiting, history storage |
| **Frontend**       | 4 days        | Chat interface, message persistence                |
| **Payments & QA**  | 3 days        | Stripe subscription, TestFlight                    |
| **TOTAL**          | **2-3 weeks** | MVP ready                                          |

### Tech Stack

```
Frontend: Next.js 16 (chat UI)
Backend: Supabase (auth, message history)
AI: Claude API (via Anthropic)
Payments: Stripe (freemium subscription)
Hosting: Vercel
```

### Monetization

| Tier     | Price     | Features                                      |
| -------- | --------- | --------------------------------------------- |
| **Free** | Free      | 3 questions/day                               |
| **Pro**  | $9.99/mo  | Unlimited questions + chat history            |
| **Pro+** | $24.99/mo | Above + birth chart context + custom guidance |

### Key Features

- **Chat interface** (clean, minimal, responsive)
- **Rate limiting** (3 questions/day free)
- **Chat history** (save conversations)
- **Share insights** (export Q&A as image)
- **Follow-up questions** (context-aware)
- **Optional birth chart** (for personalized timing)
- **Streaming responses** (real-time token delivery)

### Prompt Engineering (System Message)

```
You are Mula Oracle, a spiritual guidance AI powered by ancient wisdom and modern insight.

You have access to:
- Vedic KP astrology system
- New Orleans Vodou traditions
- Rosicrucian practical philosophy
- Western and sidereal astrology
- Global spiritual traditions

When answering:
1. Acknowledge the question with empathy
2. Provide timing-based insight (current planetary transits)
3. Give practical, actionable advice
4. Reference spiritual traditions subtly (never explicitly)
5. Encourage reflection over prediction
6. Always maintain ethical boundaries

Today's date: [DATE]
Current planetary transits: [TRANSITS]
User's chart (if provided): [CHART_DATA]
```

### API Contracts

```json
POST /api/oracle/ask
Request: { question, userId, chartData? }
Response: { answer, sources, followUpPrompts, hasMore }

GET /api/oracle/history
Response: { conversations: [{ question, answer, date }] }
```

### Marketing Viral Loop

- **Share insight:** "The Oracle says: [wisdom]" → Instagram story
- **Quote shares:** Beautiful oracle quote cards
- **Hashtag:** #AskTheOracle #MulaWisdom
- **Referral:** "Get 1 free question" for inviting friends

### Success Metrics (Week 2)

- **150+ signups** = Good interest
- **50+ paid subscriptions** = Strong monetization
- **5+ question average per user** = Engagement
- **35%+ D7 retention** = Habit forming

### File Structure

```
/src
  /api
    /oracle
      ask.ts
      history.ts
      stream.ts (real-time)
  /components
    ChatInterface.tsx
    MessageBubble.tsx
    InputBox.tsx
    HistorySidebar.tsx
  /pages
    /oracle (authenticated)
```

### Expansion Path

- Add birth chart context (auto-personalize)
- Batch questions (weekly oracle readings)
- Group oracle (team guidance)
- Custom oracle training (on company knowledge)

---

## RECOMMENDATION & DECISION FRAMEWORK

### Which Hook to Build First?

**Vote: BUILD "Daily Dasha Timer" (#1) OR "Cosmic Compatibility" (#2)**

#### Daily Dasha Timer Wins Because:

- ✅ **Existing tech:** You already have the calculation engine
- ✅ **Unique:** Nobody else does this specific timing focus
- ✅ **Daily habit:** High retention, people check daily
- ✅ **Natural premium:** Hourly updates = obvious upsell
- ✅ **Foundation:** Base for full platform expansion

#### Cosmic Compatibility Wins Because:

- ✅ **Viral by nature:** People check with everyone
- ✅ **Network effects:** Massive social sharing potential
- ✅ **Quick revenue:** $5 impulse purchase per check
- ✅ **Fast validation:** 2 weeks to know if users will pay
- ✅ **Expansion:** Base for relationship timing features

### Decision Matrix

| Factor                 | Dasha Timer | Compatibility | Moon Rituals | Remedy | Oracle  |
| ---------------------- | ----------- | ------------- | ------------ | ------ | ------- |
| **Speed to launch**    | 2-3 wks     | 2-3 wks       | 1-2 wks      | 2 wks  | 2-3 wks |
| **Revenue potential**  | $$$$        | $$$$$         | $$$          | $$$$   | $$$$    |
| **Viral potential**    | $$          | $$$$$         | $$$          | $$$$   | $$      |
| **Uses existing tech** | ✅          | ✅            | -            | -      | -       |
| **Low friction**       | -           | ✅            | ✅           | ✅     | -       |
| **Daily engagement**   | ✅          | -             | ✅           | ✅     | ✅      |
| **E-commerce natural** | -           | -             | ✅           | ✅✅   | -       |

### My Vote: START WITH DASHA TIMER

**Why:** It's the fastest path to validating your core thesis (timing-based spiritual guidance), uses your existing tech, and becomes the foundation for everything else.

**Then:** Build Compatibility Checker as second feature (cross-sell to existing users)

**Then:** Add Moon Rituals + Remedy of the Day (e-commerce focus)

---

## 2-WEEK LAUNCH PLAN (Dasha Timer)

### Week 1: Build

- **Day 1:** Finalize UI wireframes, API spec
- **Day 2-3:** Backend dasha calculation + Supabase setup
- **Day 4-5:** Frontend birth data form + timer display
- **Day 6-7:** Push notifications, Stripe integration, styling

### Week 2: Validate & Launch

- **Day 8:** TestFlight closed beta (20 friends)
- **Day 9:** Gather feedback, fix critical bugs
- **Day 10:** Launch on Product Hunt, Reddit (r/astrology), TikTok
- **Day 11-14:** Monitor metrics, optimize based on feedback

### Success = Week 2

- 100+ signups
- 10+ paid subscriptions
- 5+ social shares
- 30%+ D7 retention

**If YES:** Scale up, add features (Remedy links, multiple dashas)  
**If NO:** Pivot to Compatibility Checker, validate again

---

## DEVELOPER HANDOFF CHECKLIST

- [ ] **Review this document** and pick ONE hook to build
- [ ] **Confirm tech stack** (Next.js, Supabase, Claude, Stripe)
- [ ] **Create detailed API spec** (expand contracts above)
- [ ] **Design mobile UI** (3-5 screens, mobile-first)
- [ ] **Estimate timeline** (confirm 2-week feasibility)
- [ ] **Set up dev environment:**
  - GitHub repo + CI/CD
  - Supabase project
  - Stripe test account
  - Claude API key
  - Firebase/OneSignal for notifications
  - Vercel deployment
- [ ] **Begin Day 1 sprint** (design + core calculation)

---

## MARKETING HANDOFF CHECKLIST (Growth Team)

- [ ] **Social media templates** (beautiful shareable cards)
- [ ] **Launch announcement copy** (TikTok, Reddit, Twitter)
- [ ] **Email sequence** (to founder's existing audience)
- [ ] **Hashtag strategy** (#DashaDaily, #MyDasha, #CosmicTiming)
- [ ] **Influencer outreach** (micro-influencers in astrology space)
- [ ] **Product Hunt submission** (if building first)
- [ ] **Press release** (unique angle: AI + Vedic timing)
- [ ] **Referral program** (incentivize shares)

---

## PRODUCT ROADMAP (Post-MVP)

### Month 1: Launch Hook #1 (Dasha Timer or Compatibility)

- Validate product-market fit
- Hit 100+ signups, 10+ paying users
- Gather user feedback

### Month 2: Add Hook #2 (Compatibility or Remedies)

- Cross-sell to existing users
- Grow to 500+ signups, 50+ paying
- Revenue: $500-$1K MRR

### Month 3: Build E-Commerce Bridge

- Moon Rituals + Remedy of the Day
- Dropship product integration live
- Revenue: $2K-$5K MRR (app + products)

### Month 4+: Full Platform Integration

- Multi-hook experience (Dasha Timer + Compatibility + Remedies)
- Unified knowledge base (planet-placement indexed)
- B2B enterprise features (team compatibility)
- Path to $10K+ MRR

---

## SUCCESS METRICS & ROLLOUT

### Primary KPIs (Week 1-2)

| Metric           | Target | Action                      |
| ---------------- | ------ | --------------------------- |
| Signups          | 100+   | Scale if hit                |
| Paid conversions | 10+    | Hit paid = continue         |
| D7 retention     | 30%+   | High enough for daily habit |
| Social shares    | 5+     | Viral potential exists      |

### Secondary KPIs (Week 3+)

- Monthly revenue
- Churn rate
- NPS (Net Promoter Score)
- User feedback themes
- CAC (customer acquisition cost from organic)

---

## FILES & RESOURCES PROVIDED

✅ All 5 app hooks detailed with:

- User flow + core features
- Build timeline (2-3 weeks each)
- Tech stack recommendations
- API contracts (draft)
- Monetization strategy
- Marketing/viral loop
- Success metrics
- File structure for developer

✅ Recommendation: **Daily Dasha Timer** OR **Cosmic Compatibility**

✅ 2-week launch plan ready

✅ Handoff checklists for developer & growth team

---

## NEXT STEPS (TODAY)

1. **Founder + Developer:** Review all 5 ideas, pick ONE
2. **Confirm:** Tech stack, timeline, success metrics
3. **Design:** Mobile UI wireframes (3-5 screens)
4. **Build:** Start Day 1 sprint
5. **Growth:** Prepare launch assets (social templates, copy)

**Goal: MVP live in 2 weeks. Validate in 1 week. Scale or pivot by week 3.**

---

**All ideas are ready for immediate implementation. Pick one, build it, validate it, scale it.**
