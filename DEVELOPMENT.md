# Development Setup Guide

## Table of Contents
- [Prerequisites](#prerequisites)
- [Initial Setup](#initial-setup)
- [Development Environment](#development-environment)
- [Database Setup](#database-setup)
- [Running the Application](#running-the-application)
- [Testing](#testing)
- [Code Quality](#code-quality)
- [Troubleshooting](#troubleshooting)

## Prerequisites

### Required Software

#### Backend (Python)
- **Python 3.8+** (3.10 recommended)
- **pip** (Python package manager)
- **virtualenv** or **venv**

Check your Python version:
```bash
python3 --version
```

#### Frontend (JavaScript)
- **Node.js 14+** (16+ recommended)
- **npm 7+** (comes with Node.js)

Check your versions:
```bash
node --version
npm --version
```

#### Swiss Ephemeris
- Swiss Ephemeris data files (automated download provided)

#### Optional Tools
- **PostgreSQL 14+** (for future database integration)
- **Redis** (for caching, future feature)
- **Docker** (for containerized development)

### Development Tools

#### Code Editors (Choose One)
- **VS Code** (Recommended)
  - Extensions: Python, ESLint, Prettier, GitLens
- **PyCharm** (Professional or Community)
- **Sublime Text** with plugins

#### Version Control
- **Git 2.30+**

```bash
git --version
```

## Initial Setup

### 1. Clone Repository

```bash
# Clone the repository
git clone https://github.com/Thelastlineofcode/Astrology-Synthesis.git

# Navigate to project directory
cd Astrology-Synthesis

# Check current branch
git branch
```

### 2. Configure Git

```bash
# Set your identity
git config user.name "Your Name"
git config user.email "your.email@example.com"

# Set default branch
git config --global init.defaultBranch main
```

### 3. Set Up Environment Variables

#### Root Level
```bash
# Copy example environment file
cp .env.example .env

# Edit with your settings
nano .env  # or vim, code, etc.
```

#### Backend
```bash
cd backend
cp .env.example .env

# Edit backend-specific settings
nano .env
```

#### Frontend
```bash
cd frontend
cp .env.example .env

# Edit frontend-specific settings
nano .env
```

### 4. Backend Setup

```bash
cd backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Download Swiss Ephemeris files
cd ..
chmod +x download_ephemeris.sh
./download_ephemeris.sh
```

### 5. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Or use npm ci for clean install
npm ci
```

## Development Environment

### Backend Development

#### Virtual Environment

**Always activate before working:**
```bash
cd backend
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate  # Windows
```

**Deactivate when done:**
```bash
deactivate
```

#### Directory Structure
```
backend/
├── api/                 # API routes and endpoints
│   ├── __init__.py
│   └── routes.py
├── bmad/               # BMAD personality analysis
│   ├── api/
│   ├── engines/
│   └── utils/
├── calculations/       # Chart calculation logic
│   ├── chart_calculator.py
│   └── aspects.py
├── utils/              # Utility functions
│   └── constants.py
├── ephe/               # Swiss Ephemeris data
├── app.py              # Flask application
├── config.py           # Configuration
└── requirements.txt    # Python dependencies
```

#### Adding New Dependencies
```bash
# Activate virtual environment
source venv/bin/activate

# Install new package
pip install package-name

# Update requirements.txt
pip freeze > requirements.txt

# Commit changes
git add requirements.txt
git commit -m "chore(deps): Add package-name"
```

### Frontend Development

#### Directory Structure
```
frontend/
├── public/             # Static assets
├── src/
│   ├── components/     # React components
│   │   ├── InputForm/
│   │   ├── PlanetList/
│   │   ├── HouseTable/
│   │   └── AspectTable/
│   ├── services/       # API services
│   │   └── api.js
│   ├── utils/          # Utility functions
│   │   └── formatters.js
│   ├── App.jsx         # Main app component
│   └── index.js        # Entry point
├── package.json        # Dependencies and scripts
└── .eslintrc.json      # ESLint configuration
```

#### Adding New Dependencies
```bash
cd frontend

# Install package
npm install package-name

# Or as dev dependency
npm install --save-dev package-name

# Commit changes
git add package.json package-lock.json
git commit -m "chore(deps): Add package-name"
```

## Database Setup

### Future PostgreSQL Setup

**Note**: The application currently doesn't use a database. This section is for future reference.

#### Installation

**macOS (Homebrew)**:
```bash
brew install postgresql@14
brew services start postgresql@14
```

**Ubuntu/Debian**:
```bash
sudo apt-get install postgresql-14
sudo systemctl start postgresql
```

#### Database Creation
```bash
# Connect to PostgreSQL
psql postgres

# Create database and user
CREATE DATABASE astrology_db;
CREATE USER astrology_user WITH ENCRYPTED PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE astrology_db TO astrology_user;

# Exit
\q
```

#### Update .env
```bash
DATABASE_URL=postgresql://astrology_user:your_password@localhost:5432/astrology_db
```

### Schema Design (Future)

Tables to be implemented:
- `users` - User accounts
- `charts` - Saved birth charts
- `calculations` - Cached calculations
- `sessions` - User sessions

## Running the Application

### Development Mode

#### Option 1: Separate Terminals

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate
python app.py
```
Backend runs on: http://localhost:5000

**Terminal 2 - Frontend:**
```bash
cd frontend
npm start
```
Frontend runs on: http://localhost:3001

#### Option 2: Using tmux (Advanced)

```bash
# Start tmux session
tmux new -s astrology-dev

# Split terminal
Ctrl-b %  # vertical split
Ctrl-b "  # horizontal split

# Navigate between panes
Ctrl-b arrow keys

# In one pane: run backend
cd backend && source venv/bin/activate && python app.py

# In other pane: run frontend
cd frontend && npm start
```

### Production Mode

```bash
# Build frontend
cd frontend
npm run build

# Serve with production server
# (Configure nginx or use gunicorn for Flask)
```

## Testing

### Backend Tests

```bash
cd backend
source venv/bin/activate

# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest test_astrology_app.py

# Run specific test
pytest test_astrology_app.py::test_health_check

# View coverage report
open htmlcov/index.html
```

### Frontend Tests

```bash
cd frontend

# Run tests in watch mode
npm test

# Run all tests once
npm test -- --watchAll=false

# Run with coverage
npm run test:coverage

# View coverage
open coverage/lcov-report/index.html
```

### Integration Tests

```bash
# From project root
./run_all_tests.sh
```

## Code Quality

### Frontend Linting and Formatting

```bash
cd frontend

# Run ESLint
npm run lint

# Fix ESLint issues automatically
npm run lint:fix

# Run Prettier
npm run format

# Check formatting without changing files
npm run format:check
```

### Backend Linting and Formatting

```bash
cd backend
source venv/bin/activate

# Run flake8
flake8 .

# Run black (auto-format)
black .

# Check black without changes
black --check .

# Run isort (import sorting)
isort .

# Type checking with mypy
mypy .
```

### Pre-commit Checks

Before committing, run:
```bash
# Frontend
cd frontend
npm run lint && npm run format:check && npm test -- --watchAll=false

# Backend
cd backend
source venv/bin/activate
flake8 . && black --check . && pytest
```

## Troubleshooting

### Backend Issues

#### "Module not found" Error
```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

#### "Swiss Ephemeris file not found"
```bash
cd Astrology-Synthesis
./download_ephemeris.sh

# Or manually:
cd backend/ephe
curl -O https://www.astro.com/ftp/swisseph/ephe/sepl_18.se1
curl -O https://www.astro.com/ftp/swisseph/ephe/semo_18.se1
curl -O https://www.astro.com/ftp/swisseph/ephe/seas_18.se1
```

#### Port 5000 Already in Use
```bash
# Kill process on port 5000
lsof -ti:5000 | xargs kill -9

# Or use different port
python app.py --port 5001
```

### Frontend Issues

#### "Cannot connect to backend"
- Verify backend is running on port 5000
- Check proxy setting in `package.json`
- Check CORS settings in `backend/app.py`
- Verify `REACT_APP_API_URL` in `.env`

#### npm Install Fails
```bash
# Clear npm cache
npm cache clean --force

# Remove node_modules and package-lock.json
rm -rf node_modules package-lock.json

# Reinstall
npm install
```

#### Port 3001 Already in Use
```bash
# Kill process on port 3001
lsof -ti:3001 | xargs kill -9

# Or specify different port
PORT=3002 npm start
```

### General Issues

#### Git Issues
```bash
# Reset to clean state (careful!)
git reset --hard HEAD
git clean -fd

# Update from remote
git fetch origin
git pull origin develop
```

#### Permission Denied
```bash
# Make script executable
chmod +x script_name.sh

# Fix ownership
sudo chown -R $USER:$USER .
```

## Development Workflow

### Daily Workflow

1. **Start of day**:
   ```bash
   git checkout develop
   git pull origin develop
   git checkout -b feature/your-feature
   ```

2. **During development**:
   - Run backend: `cd backend && source venv/bin/activate && python app.py`
   - Run frontend: `cd frontend && npm start`
   - Run tests frequently
   - Commit regularly with meaningful messages

3. **Before committing**:
   ```bash
   # Lint and format
   cd frontend && npm run lint:fix && npm run format
   cd backend && black . && isort .
   
   # Run tests
   cd frontend && npm test -- --watchAll=false
   cd backend && pytest
   ```

4. **End of day**:
   ```bash
   git add .
   git commit -m "feat(scope): description of changes"
   git push origin feature/your-feature
   ```

### Useful Commands

```bash
# Check application status
curl http://localhost:5000/api/health

# View logs
tail -f logs/backend.log

# Monitor file changes
watch -n 1 ls -lh backend/

# Find processes on ports
lsof -i :5000
lsof -i :3001
```

## Additional Resources

- [README.md](./README.md) - Project overview
- [CONTRIBUTING.md](./CONTRIBUTING.md) - Git workflow
- [CHART_CALCULATOR_IMPLEMENTATION.md](./CHART_CALCULATOR_IMPLEMENTATION.md) - Technical details
- [BMAD_USAGE_GUIDE.md](./BMAD_USAGE_GUIDE.md) - BMAD integration

## Getting Help

- Check existing issues on GitHub
- Read documentation in `docs/` folder
- Ask in team chat or create GitHub issue
- Review commit history for similar features

---

**Last Updated**: October 28, 2025  
**Maintained By**: Development Team

Happy Coding! 🌟
