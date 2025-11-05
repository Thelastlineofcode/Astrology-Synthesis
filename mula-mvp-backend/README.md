# Mula Dasha Timer MVP - Backend

FastAPI backend for the Mula Dasha Timer MVP.

## Features

- **Authentication**: JWT + Google OAuth + Apple Sign-In
- **Birth Charts**: Calculate and store Vedic birth charts
- **Dasha Periods**: Vimshottari Dasha timeline calculations
- **AI Advisors**: Papa Legba and other personalities via Perplexity API
- **Notifications**: Push notifications via Firebase Cloud Messaging

## Setup

### 1. Install Dependencies

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env with your credentials
```

### 3. Initialize Database

```bash
# Local PostgreSQL
createdb mula_mvp

# Or use Railway/Render for cloud PostgreSQL
```

### 4. Run Development Server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Visit: http://localhost:8000/docs for API documentation

## Project Structure

```
mula-mvp-backend/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── auth.py          # Authentication endpoints
│   │       ├── chart.py         # Birth chart endpoints
│   │       ├── dasha.py         # Dasha period endpoints
│   │       ├── advisor.py       # AI advisor endpoints
│   │       └── notifications.py # Notification endpoints
│   ├── core/
│   │   ├── config.py           # Settings
│   │   └── database.py         # Database setup
│   ├── models/
│   │   └── database.py         # SQLAlchemy models
│   ├── schemas/
│   │   └── ...                 # Pydantic schemas (to be added)
│   └── main.py                 # FastAPI app
├── tests/
│   └── ...                      # Tests (to be added)
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Database Schema

### Users

- Authentication (email/password, Google, Apple)
- Birth data (date, time, location)
- Notification preferences

### Birth Charts

- Calculated chart data (planets, houses, etc.)
- Current dasha period (denormalized for speed)

### Dasha Periods

- Full Vimshottari timeline
- Mahadasha, Antardasha, Pratyantardasha
- Interpretations and themes

### Advisors

- Papa Legba, Marie Laveau, etc.
- Perplexity API system prompts
- Knowledge base context

### Messages

- User questions to advisors
- AI-generated responses
- Conversation history

### Notification Tokens

- FCM tokens for push notifications
- User preferences

## Deployment

### Railway

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Deploy
railway up
```

### Render

1. Connect GitHub repo
2. Set environment variables
3. Deploy automatically on push

## Next Steps

1. Implement authentication logic (JWT, OAuth)
2. Integrate Vedic calculation engine
3. Connect Perplexity API for advisors
4. Set up Firebase Cloud Messaging
5. Add comprehensive tests
6. Deploy to production

## API Endpoints

See full documentation at `/docs` when server is running.

### Authentication

- `POST /api/v1/auth/signup` - User registration
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/google` - Google OAuth
- `POST /api/v1/auth/apple` - Apple Sign-In

### Birth Charts

- `POST /api/v1/chart/create` - Create birth chart
- `GET /api/v1/chart/{id}` - Get chart by ID

### Dasha Periods

- `GET /api/v1/dasha/current` - Current dasha
- `GET /api/v1/dasha/timeline` - Full timeline
- `GET /api/v1/dasha/meanings/{planet}` - Planet meanings

### Advisors

- `GET /api/v1/advisor/list` - List advisors
- `POST /api/v1/advisor/query` - Ask question
- `GET /api/v1/advisor/history` - Conversation history

### Notifications

- `POST /api/v1/notifications/register` - Register FCM token
- `PUT /api/v1/notifications/preferences` - Update preferences
- `GET /api/v1/notifications/preferences` - Get preferences
