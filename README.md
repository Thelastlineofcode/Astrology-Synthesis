# Roots Revealed - Full-Stack Astrological Analysis System

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
CREATE DATABASE roots_revealed_db;
CREATE USER roots_revealed_user WITH ENCRYPTED PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE roots_revealed_db TO roots_revealed_user;
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
Roots-Revealed/
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
DB_NAME=roots_revealed_db
DB_USER=roots_revealed_user
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

### Interactive Documentation

The API includes comprehensive interactive documentation:

- **Swagger UI**: [http://localhost:5000/api-docs](http://localhost:5000/api-docs)
- **OpenAPI Spec**: [http://localhost:5000/api-docs.json](http://localhost:5000/api-docs.json)
- **Postman Collection**: `backend/Roots-Revealed-API.postman_collection.json`

### Base URL

```
http://localhost:5000/api
```

### Quick Reference

#### Authentication Endpoints
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `POST /api/auth/logout` - Logout user (requires auth)
- `POST /api/auth/refresh` - Refresh JWT token (requires auth)

#### Chart Management Endpoints
- `GET /api/charts` - Get all charts (paginated, requires auth)
- `POST /api/charts` - Create new chart (requires auth)
- `GET /api/charts/:id` - Get specific chart (requires auth)
- `PUT /api/charts/:id` - Update chart (requires auth)
- `DELETE /api/charts/:id` - Delete chart (requires auth)

#### Calculation & Interpretation Endpoints
- `POST /api/charts/calculate` - Calculate birth chart (requires auth)
- `GET /api/charts/:id/interpretation` - Get BMAD & Symbolon interpretation (requires auth)

#### Health Check
- `GET /api/health` - API health status
- `GET /` - API information

For detailed request/response examples and schemas, visit the **Swagger UI** when the server is running.

### Using the API

#### 1. Register & Login

```bash
# Register
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"password123","name":"John Doe"}'

# Login
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"password123"}'
```

#### 2. Create a Chart

```bash
curl -X POST http://localhost:5000/api/charts \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My Birth Chart",
    "birthDate": "1990-01-15",
    "birthTime": "14:30",
    "latitude": 40.7128,
    "longitude": -74.0060
  }'
```

#### 3. Calculate Chart Data

```bash
curl -X POST http://localhost:5000/api/charts/calculate \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "birthDate": "1990-01-15",
    "birthTime": "14:30",
    "latitude": 40.7128,
    "longitude": -74.0060,
    "houseSystem": "Placidus"
  }'
```

### Importing Postman Collection

1. Open Postman
2. Click "Import" button
3. Select `backend/Roots-Revealed-API.postman_collection.json`
4. The collection includes all endpoints with example requests
5. Set the `baseUrl` variable to your server URL
6. Authenticate using Register/Login to auto-populate `authToken`

### Authentication

Protected endpoints require a JWT token in the Authorization header:

```
Authorization: Bearer <your-jwt-token>
```

Tokens are obtained from `/api/auth/register` or `/api/auth/login` responses and can be refreshed using `/api/auth/refresh`.

### Pagination

List endpoints support pagination via query parameters:

```
GET /api/charts?page=1&limit=10
```

Response includes pagination metadata:

```json
{
  "success": true,
  "data": [...],
  "pagination": {
    "page": 1,
    "limit": 10,
    "total": 25,
    "totalPages": 3
  }
}
```

### Error Handling

All endpoints return consistent error responses:

```json
{
  "success": false,
  "error": {
    "message": "Error description",
    "statusCode": 400
  }
}
```

Common status codes:
- `200` - Success
- `201` - Created
- `400` - Bad Request (validation error)
- `401` - Unauthorized (missing/invalid token)
- `404` - Not Found
- `500` - Internal Server Error

### Example: Complete Workflow

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
psql -U roots_revealed_user -d roots_revealed_db
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

### Development Guides
- [CONTRIBUTING.md](./CONTRIBUTING.md) - Git workflow and contribution guidelines
- [DEVELOPMENT.md](./DEVELOPMENT.md) - Detailed development setup
- [DATABASE_SCHEMA.md](./DATABASE_SCHEMA.md) - Database design and schema

### Design System
- [COLOR_PALETTE_AND_DESIGN_SYSTEM.md](./COLOR_PALETTE_AND_DESIGN_SYSTEM.md) - Comprehensive design system, color palette, typography, and component patterns
- [ACCESSIBILITY_TESTING_GUIDE.md](./ACCESSIBILITY_TESTING_GUIDE.md) - WCAG 2.1 compliance and accessibility testing guidelines
- [Quick Reference Guide](./docs/redesign/QUICK_REFERENCE.md) - Quick reference for developers

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
