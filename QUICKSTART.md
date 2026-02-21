# Quick Start Guide

## Prerequisites

1. **Python 3.9+** installed
2. **Node.js 18+** installed
3. **PostgreSQL** running (or use Docker)
4. **MongoDB** running (or use Docker)
5. **Clerk account** - Sign up at [clerk.com](https://clerk.com)
6. **API Keys**:
   - Alpha Vantage: [alphavantage.co](https://www.alphavantage.co/support/#api-key)
   - The Odds API: [the-odds-api.com](https://the-odds-api.com/)

## Quick Setup (5 minutes)

### 1. Backend Setup

```bash
cd backend
python -m venv venv
# Windows: venv\Scripts\activate
# Linux/Mac: source venv/bin/activate
pip install -r requirements.txt
```

Create `backend/.env` file:
```env
CLERK_SECRET_KEY=sk_test_...
CLERK_PUBLISHABLE_KEY=pk_test_...
MONGODB_URI=mongodb://localhost:27017
MONGODB_DB_NAME=predict_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=predict_db
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
ALPHA_VANTAGE_API_KEY=your_key_here
THE_ODDS_API_KEY=your_key_here
CORS_ORIGINS=http://localhost:5173
```

Initialize database:
```bash
python init_db.py
```

Start backend:
```bash
uvicorn main:app --reload
```

### 2. Frontend Setup

```bash
cd frontend
npm install
```

Create `frontend/.env` file:
```env
VITE_CLERK_PUBLISHABLE_KEY=pk_test_...
VITE_API_URL=http://localhost:8000
```

Start frontend:
```bash
npm run dev
```

### 3. Access the App

- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Docker Setup (Alternative)

```bash
# Create .env files first (see above)
docker-compose up
```

## First Steps

1. Sign up/Sign in at the landing page
2. Navigate to Dashboard
3. Try a stock prediction (e.g., AAPL, MSFT)
4. Browse sports predictions
5. Save some picks to your profile

## Troubleshooting

### Backend won't start
- Check PostgreSQL is running: `pg_isready`
- Check MongoDB is running: `mongosh --eval "db.adminCommand('ping')"`
- Verify all environment variables are set

### Frontend won't connect to backend
- Check `VITE_API_URL` matches backend URL
- Check CORS settings in backend `.env`
- Check browser console for errors

### Authentication issues
- Verify Clerk keys are correct
- Check Clerk dashboard for application status
- Ensure frontend and backend use same Clerk application

## Next Steps

- Read the full README.md for detailed documentation
- Check API documentation at /docs endpoint
- Review code structure in app/ directory
- Run tests: `pytest` in backend directory
