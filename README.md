# Astrology Synthesis - Full-Stack Astrological Analysis System

A modern full-stack astrology application built with Next.js, Node.js/Express, TypeScript, and PostgreSQL.

## 🏗️ Architecture

### Technology Stack

#### Frontend
- **Framework**: Next.js 16 with App Router
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **State Management**: React Context API / Zustand (future)
- **Testing**: Jest + React Testing Library

#### Backend
- **Runtime**: Node.js 20+
- **Framework**: Express.js
- **Language**: TypeScript
- **Database**: PostgreSQL 14+
- **Authentication**: JWT (JSON Web Tokens)
- **Testing**: Jest + Supertest

#### DevOps
- **Version Control**: Git
- **Package Manager**: npm
- **Linting**: ESLint
- **Formatting**: Prettier
- **CI/CD**: GitHub Actions (future)

## 📋 Prerequisites

### Required Software

- **Node.js**: v18.0.0 or higher
- **npm**: v9.0.0 or higher
- **PostgreSQL**: v14.0 or higher
- **Git**: v2.30 or higher

### Verify Installations

```bash
node --version  # Should be v18+
npm --version   # Should be v9+
psql --version  # Should be v14+
git --version   # Should be v2.30+
```

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/Thelastlineofcode/Astrology-Synthesis.git
cd Astrology-Synthesis
```

### 2. Set Up PostgreSQL Database

```bash
# Start PostgreSQL service
# macOS (Homebrew):
brew services start postgresql@14

# Linux (Ubuntu/Debian):
sudo systemctl start postgresql

# Create database and user
psql postgres
```

In the PostgreSQL console:
```sql
CREATE DATABASE astrology_db;
CREATE USER astrology_user WITH ENCRYPTED PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE astrology_db TO astrology_user;
\q
```

### 3. Backend Setup

```bash
cd backend

# Copy environment file
cp .env.example .env

# Edit .env with your database credentials
nano .env  # or use your preferred editor

# Install dependencies
npm install

# Build TypeScript
npm run build

# Run tests
npm test

# Start development server
npm run dev
```

Backend will run on: **http://localhost:5000**

### 4. Frontend Setup

```bash
cd ../frontend

# Copy environment file
cp .env.local.example .env.local

# Install dependencies
npm install

# Run tests
npm test

# Start development server
npm run dev
```

Frontend will run on: **http://localhost:3000**

## 📁 Project Structure

```
Astrology-Synthesis/
├── backend/                    # Node.js/Express API
│   ├── src/
│   │   ├── config/            # Configuration files
│   │   ├── controllers/       # Request handlers
│   │   ├── middleware/        # Express middleware
│   │   ├── models/            # Database models
│   │   ├── routes/            # API routes
│   │   ├── services/          # Business logic
│   │   ├── types/             # TypeScript types
│   │   ├── utils/             # Utility functions
│   │   ├── __tests__/         # Tests
│   │   └── index.ts           # Entry point
│   ├── dist/                  # Compiled JavaScript
│   ├── .env.example           # Environment template
│   ├── package.json
│   ├── tsconfig.json
│   └── jest.config.js
│
├── frontend/                   # Next.js Application
│   ├── src/
│   │   ├── app/               # Next.js App Router
│   │   │   ├── __tests__/     # Page tests
│   │   │   ├── layout.tsx     # Root layout
│   │   │   ├── page.tsx       # Home page
│   │   │   └── globals.css    # Global styles
│   │   ├── components/        # React components
│   │   ├── lib/               # Utility libraries
│   │   └── types/             # TypeScript types
│   ├── public/                # Static assets
│   ├── .env.local.example     # Environment template
│   ├── package.json
│   ├── tsconfig.json
│   ├── tailwind.config.ts
│   └── jest.config.ts
│
├── .env.example               # Root environment template
├── .gitignore
├── README.md
├── CONTRIBUTING.md            # Contribution guidelines
├── DEVELOPMENT.md             # Development setup guide
└── DATABASE_SCHEMA.md         # Database schema documentation
```

## 🔑 Environment Variables

### Backend (.env)

```env
# Server
PORT=5000
NODE_ENV=development

# JWT
JWT_SECRET=your-secret-key-change-in-production
JWT_EXPIRES_IN=24h

# Database
DB_HOST=localhost
DB_PORT=5432
DB_NAME=astrology_db
DB_USER=astrology_user
DB_PASSWORD=your_password_here

# CORS
CORS_ORIGIN=http://localhost:3000
```

### Frontend (.env.local)

```env
NEXT_PUBLIC_API_URL=http://localhost:5000
NEXT_PUBLIC_DEBUG=true
```

## 🧪 Testing

### Backend Tests

```bash
cd backend

# Run all tests
npm test

# Run tests in watch mode
npm run test:watch

# Run tests with coverage
npm test -- --coverage
```

### Frontend Tests

```bash
cd frontend

# Run all tests
npm test

# Run tests in watch mode
npm run test:watch

# Run tests with coverage
npm run test:coverage
```

## 📖 API Documentation

### Base URL

```
http://localhost:5000/api
```

### Endpoints

#### Health Check
```http
GET /api/health
```

**Response:**
```json
{
  "success": true,
  "message": "API is healthy",
  "timestamp": "2025-10-28T20:00:00.000Z",
  "uptime": 1234.56
}
```

#### Authentication

##### Register
```http
POST /api/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123",
  "name": "John Doe"
}
```

##### Login
```http
POST /api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Login successful",
  "data": {
    "user": {
      "id": "123",
      "email": "user@example.com",
      "name": "John Doe"
    },
    "token": "jwt.token.here"
  }
}
```

#### Charts (Protected - Requires Authentication)

##### Get All Charts
```http
GET /api/charts
Authorization: Bearer <token>
```

##### Create Chart
```http
POST /api/charts
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "My Birth Chart",
  "birthDate": "1990-01-15",
  "birthTime": "14:30",
  "latitude": 40.7128,
  "longitude": -74.0060
}
```

## 🔧 Development

### Code Quality

```bash
# Lint backend
cd backend && npm run lint

# Lint frontend
cd frontend && npm run lint

# Format code
npm run format
```

### Building for Production

#### Backend
```bash
cd backend
npm run build
npm start
```

#### Frontend
```bash
cd frontend
npm run build
npm start
```

## 🛠️ Troubleshooting

### Database Connection Issues

1. Verify PostgreSQL is running:
```bash
pg_isready
```

2. Check database exists:
```bash
psql -U astrology_user -d astrology_db
```

3. Verify credentials in `.env` file

### Port Already in Use

```bash
# Kill process on port 5000 (backend)
lsof -ti:5000 | xargs kill -9

# Kill process on port 3000 (frontend)
lsof -ti:3000 | xargs kill -9
```

### Module Not Found Errors

```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

## 📚 Additional Documentation

- [CONTRIBUTING.md](./CONTRIBUTING.md) - Git workflow and contribution guidelines
- [DEVELOPMENT.md](./DEVELOPMENT.md) - Detailed development setup
- [DATABASE_SCHEMA.md](./DATABASE_SCHEMA.md) - Database design and schema

## 🗺️ Roadmap

### Phase 1: Foundation (Current)
- [x] Project setup with Next.js and Express
- [x] TypeScript configuration
- [x] JWT authentication
- [x] PostgreSQL integration ready
- [x] Testing frameworks
- [x] Code quality tools (ESLint, Prettier)

### Phase 2: Core Features (Next)
- [ ] User profile management
- [ ] Chart calculation engine
- [ ] Real database integration
- [ ] Chart storage and retrieval
- [ ] API rate limiting

### Phase 3: Advanced Features
- [ ] Chart visualization
- [ ] Aspect calculations
- [ ] Transit calculations
- [ ] Synastry analysis
- [ ] PDF chart reports

### Phase 4: Production
- [ ] Deployment configuration
- [ ] CI/CD pipeline
- [ ] Performance optimization
- [ ] Security hardening
- [ ] Monitoring and logging

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.

## 📄 License

ISC License

## 👥 Authors

- Product Management Team
- Development Team

## 📞 Support

For issues and questions:
- Create an issue on GitHub
- Contact the development team

---

**Last Updated**: October 28, 2025  
**Version**: 1.0.0  
**Status**: Development
