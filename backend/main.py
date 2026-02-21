"""FastAPI application entry point."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import connect_mongodb, disconnect_mongodb, Base, engine
from app.routers import auth, stocks, sports, user, analytics

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="Predict API",
    description="Stock and Sports Market Predictions API",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(stocks.router)
app.include_router(sports.router)
app.include_router(user.router)
app.include_router(analytics.router)


@app.on_event("startup")
async def startup_event():
    """Initialize connections on startup."""
    await connect_mongodb()


@app.on_event("shutdown")
async def shutdown_event():
    """Clean up connections on shutdown."""
    await disconnect_mongodb()


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Predict API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
