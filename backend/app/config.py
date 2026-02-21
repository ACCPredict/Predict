"""Application configuration using Pydantic settings."""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Clerk Configuration
    clerk_secret_key: str
    clerk_publishable_key: str
    
    # MongoDB Configuration
    mongodb_uri: str
    mongodb_db_name: str = "predict_db"
    
    # PostgreSQL Configuration
    postgres_user: str = "postgres"
    postgres_password: str = "postgres"
    postgres_db: str = "predict_db"
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    
    # External API Keys
    alpha_vantage_api_key: str
    the_odds_api_key: str
    
    # Application Settings
    environment: str = "development"
    cors_origins: str = "http://localhost:5173,http://localhost:3000"
    
    @property
    def postgres_url(self) -> str:
        """Construct PostgreSQL connection URL."""
        return f"postgresql://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins from comma-separated string."""
        return [origin.strip() for origin in self.cors_origins.split(",")]
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
