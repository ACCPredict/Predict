# Quick Setup Guide

## Initial Setup

### 1. Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
copy .env.example .env  # Windows
# or
cp .env.example .env    # Linux/Mac

# Edit .env file with your MongoDB URI and API keys
```

### 2. MongoDB Setup

You can either:
- Use a local MongoDB instance: `mongodb://localhost:27017`
- Use MongoDB Atlas (cloud): Get connection string from MongoDB Atlas dashboard

### 3. Frontend Setup

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install
```

## Running the Application

### Start Backend

```bash
cd backend
# Make sure virtual environment is activated
uvicorn main:app --reload
```

Backend will run on `http://localhost:8000`

### Start Frontend

```bash
cd frontend
npm run dev
```

Frontend will run on `http://localhost:3000`

## API Documentation

Once the backend is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Testing the API

You can test the API endpoints using:
- Swagger UI (interactive)
- Postman
- curl commands

Example:
```bash
curl http://localhost:8000/api/sportsbooks
```

## Next Steps

1. **Get API Keys**: Obtain API keys from sportsbook providers
2. **Implement API Integrations**: Update `sportsbook_api.py` with actual API calls
3. **Collect Historical Data**: Set up data collection scripts
4. **Test Features**: Test line comparisons, arbitrage detection, and predictions
