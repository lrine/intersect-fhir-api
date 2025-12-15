"""
Application Configuration
Reads from environment variables and .env file
"""
from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from typing import List
import os


class Settings(BaseSettings):
    """Application settings from environment"""
    
    # Application
    app_name: str = "Intersect FHIR API"
    app_version: str = "1.0.0"
    debug: bool = False
    environment: str = "production"
    
    # API
    api_prefix: str = "/api/v1"
    host: str = "0.0.0.0"
    port: int = 8000
    
    # MongoDB / Cosmos DB
    mongodb_url: str
    mongodb_database: str = "intersect_fhir"
    mongodb_min_pool_size: int = 10
    mongodb_max_pool_size: int = 100
    
    # JWT Authentication
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # CORS
    allowed_origins: str = "http://localhost:3000"
    
    @property
    def allowed_origins_list(self) -> List[str]:
        """Parse comma-separated origins into list"""
        return [origin.strip() for origin in self.allowed_origins.split(",")]
    
    # Logging
    log_level: str = "INFO"
    log_file: str = "logs/intersect-fhir-api.log"
    
    # Feature Flags
    enable_auth: bool = True
    enable_rate_limiting: bool = True
    enable_audit_logging: bool = True
    
    # Wearable Integration
    samsung_health_api_key: str = ""
    samsung_health_client_secret: str = ""
    
    # External Services
    genomics_lab_api_url: str = ""
    genomics_lab_api_key: str = ""

    model_config = ConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore"
    )


# Global settings instance
settings = Settings()
