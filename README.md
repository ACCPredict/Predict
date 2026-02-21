# Predict - Stock & Sports Market Predictions

A full-stack web application that generates probabilistic predictions for stocks and sports betting markets. Predictions are informational only.

## Project Overview

This application provides AI-powered predictions with confidence scores for:
- **Stock Market**: Logistic regression models analyzing price movements and technical indicators
- **Sports Betting**: Odds-based predictions adjusted with team ratings

## Project Managers

- Luke Abraham
- Andrew Johnson

## Tech Stack

### Frontend
- **React** with **Vite**
- **Clerk** for authentication
- **Recharts** for data visualization
- **Axios** for API calls

### Backend
- **FastAPI** (Python)
- **PostgreSQL** (via SQLAlchemy) for users, picks, and accuracy metrics
- **MongoDB** for raw API data and prediction logs
- **JWT** validation with Clerk tokens

### External APIs
- **Alpha Vantage** for stock data
- **The Odds API** for sports odds

## Project Structure

```
predict/
├── frontend/          # React frontend
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── App.jsx
│   ├── package.json
│   └── Dockerfile
├── backend/           # Python FastAPI backend
│   ├── app/
│   │   ├── routers/  # API endpoints
│   │   ├── services/  # Business logic
│   │   ├── models.py  # SQLAlchemy models
│   │   └── schemas.py # Pydantic schemas
│   ├── tests/         # Unit and API tests
│   ├── main.py
│   ├── requirements.txt
│   └── Dockerfile
├── docker-compose.yml
└── README.md
```

## Local Setup

### Prerequisites

- Python 3.9+
- Node.js 18+
- Docker and Docker Compose (optional, for containerized setup)
- PostgreSQL (if not using Docker)
- MongoDB (if not using Docker)

### Option 1: Docker Compose (Recommended)

1. **Clone the repository** (if applicable)

2. **Set up environment variables**:
   - Copy `.env.example` files in both `backend/` and `frontend/` directories
   - Fill in your API keys:
     - Clerk Secret Key and Publishable Key
     - Alpha Vantage API Key
     - The Odds API Key

3. **Start all services**:
   ```bash
   docker-compose up
   ```

   This will start:
   - PostgreSQL on port 5432
   - MongoDB on port 27017
   - Backend API on port 8000
   - Frontend on port 5173

### Option 2: Manual Setup

#### Backend Setup

1. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   ```

3. **Activate virtual environment**:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up environment variables**:
   - Copy `.env.example` to `.env`
   - Update with your API keys and database credentials

6. **Set up databases**:
   - Ensure PostgreSQL is running and create database `predict_db`
   - Ensure MongoDB is running

7. **Run database migrations** (tables are created automatically on first run):
   ```bash
   python -c "from app.database import Base, engine; Base.metadata.create_all(bind=engine)"
   ```

8. **Start the server**:
   ```bash
   uvicorn main:app --reload
   ```

   Backend will be available at `http://localhost:8000`

#### Frontend Setup

1. **Navigate to frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Set up environment variables**:
   - Copy `.env.example` to `.env`
   - Add your Clerk Publishable Key and backend URL

4. **Start development server**:
   ```bash
   npm run dev
   ```

   Frontend will be available at `http://localhost:5173`

## Environment Variables

### Backend (.env)

```env
# Clerk Configuration
CLERK_SECRET_KEY=your_clerk_secret_key_here
CLERK_PUBLISHABLE_KEY=your_clerk_publishable_key_here

# Database Configuration
MONGODB_URI=mongodb://localhost:27017
MONGODB_DB_NAME=predict_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=predict_db
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

# External API Keys
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key_here
THE_ODDS_API_KEY=your_the_odds_api_key_here

# Application Settings
ENVIRONMENT=development
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

### Frontend (.env)

```env
VITE_CLERK_PUBLISHABLE_KEY=your_clerk_publishable_key_here
VITE_API_URL=http://localhost:8000
```

## API Endpoints

### Authentication
- `GET /auth/verify` - Verify authentication token

### Stock Predictions
- `GET /stocks/predictions?symbol=AAPL` - Get stock prediction for a symbol

### Sports Predictions
- `GET /sports/predictions?sport=basketball_nba` - Get sports predictions

### User Picks
- `POST /user/picks` - Save a user pick
- `GET /user/picks` - Get all user picks

### Analytics
- `GET /analytics/accuracy` - Get accuracy metrics

## API Documentation

Once the backend is running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Testing

### Backend Tests

```bash
cd backend
pytest
```

Tests include:
- Unit tests for prediction models
- API smoke tests

## Deployment on Free Tiers

### Backend Deployment

**Recommended Platforms:**
- **Render** (Free tier available)
- **Railway** (Free tier available)
- **Fly.io** (Free tier available)

**Steps:**
1. Push code to GitHub
2. Connect repository to deployment platform
3. Set environment variables in platform dashboard
4. Deploy

**Database Options:**
- **PostgreSQL**: Use free tier from Supabase, Neon, or ElephantSQL
- **MongoDB**: Use MongoDB Atlas free tier (M0 cluster)

### Frontend Deployment

**Recommended Platforms:**
- **Vercel** (Free tier, excellent for React)
- **Netlify** (Free tier)
- **GitHub Pages** (Free, static hosting)

**Steps:**
1. Build the frontend: `npm run build`
2. Deploy `dist/` folder to hosting platform
3. Set environment variables in platform dashboard

### Clerk Setup

1. Sign up at [clerk.com](https://clerk.com)
2. Create a new application
3. Get your Publishable Key and Secret Key
4. Add them to environment variables

### API Keys

1. **Alpha Vantage**: Sign up at [alphavantage.co](https://www.alphavantage.co/support/#api-key) (free tier: 5 API calls/minute)
2. **The Odds API**: Sign up at [the-odds-api.com](https://the-odds-api.com/) (free tier: 500 requests/month)

## Features

### Stock Predictions
- Enter any stock symbol (e.g., AAPL, MSFT, GOOGL)
- View probability, confidence, and direction prediction
- See current price and price target
- Save predictions as picks

### Sports Predictions
- Browse predictions by sport (NBA, NFL, NHL, MLB, etc.)
- View team predictions with odds
- See implied probabilities
- Save favorite predictions

### Dashboard
- View accuracy metrics
- See historical accuracy charts
- Review recent saved picks

### Profile
- View user information
- See all saved picks
- Track prediction history

## Security

- All protected routes require valid Clerk JWT tokens
- Passwords are never stored (handled by Clerk)
- All secrets stored in environment variables
- CORS configured for frontend origins only

## Coding Standards

- Clear file naming conventions
- Business logic separated from routes
- Comments added where needed
- Modular router structure
- Type hints in Python code

## Contributing

1. Follow the coding standards
2. Add tests for new features
3. Update documentation as needed
4. Ensure all tests pass before submitting

## License

This project is for informational purposes only. Predictions should not be used as financial or betting advice.
