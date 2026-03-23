"""
Configuration management for Astrology API
Simple hardcoded configuration with no environment variables needed
"""
from typing import List


class Settings:
    """Application settings - no environment variables or .env files needed"""
    
    # API Settings
    api_title: str = "Vedic Astrology API"
    api_version: str = "1.0.0"
    api_description: str = "Professional REST API for Vedic Astrology Birth Chart Calculations"
    
    # Server Settings
    host: str = "0.0.0.0"
    port: int = 12909
    reload: bool = True
    log_level: str = "INFO"
    debug: bool = False
    
    # Paths
    ephemeris_path: str = "./ephemeris"
    
    # Defaults
    default_timezone_offset: float = 5.5
    
    # CORS
    enable_cors: bool = True
    cors_origins: List[str] = ["*"]
    
    # Rate Limiting
    enable_rate_limiting: bool = True
    rate_limit_requests: int = 100
    rate_limit_period: int = 3600
    
    # Caching
    enable_cache: bool = True
    cache_ttl: int = 3600
    
    # Workers (for production)
    workers: int = 4


# Create settings instance
settings = Settings()


def get_settings() -> Settings:
    """Get application settings"""
    return settings
