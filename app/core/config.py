import os
from typing import List
from dotenv import load_dotenv
from pydantic import BaseSettings as PydanticBaseSettings

load_dotenv()

class Settings(PydanticBaseSettings):
    PROJECT_NAME: str = "Contacts API"
    API_V1_PREFIX: str = "/api/v1"
    
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-for-development-only")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/contacts")

    CORS_ORIGINS: List[str] = ["*"]
    
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    
    CLOUDINARY_CLOUD_NAME: str = os.getenv("CLOUDINARY_CLOUD_NAME", "")
    CLOUDINARY_API_KEY: str = os.getenv("CLOUDINARY_API_KEY", "")
    CLOUDINARY_API_SECRET: str = os.getenv("CLOUDINARY_API_SECRET", "")
    
    MAIL_USERNAME: str = os.getenv("MAIL_USERNAME", "")
    MAIL_PASSWORD: str = os.getenv("MAIL_PASSWORD", "")
    MAIL_FROM: str = os.getenv("MAIL_FROM", "")
    MAIL_PORT: int = int(os.getenv("MAIL_PORT", 587))
    MAIL_SERVER: str = os.getenv("MAIL_SERVER", "smtp.gmail.com")
    MAIL_FROM_NAME: str = os.getenv("MAIL_FROM_NAME", "Contacts App")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()

API_V1_PREFIX = settings.API_V1_PREFIX
PROJECT_NAME = settings.PROJECT_NAME
DATABASE_URL = settings.DATABASE_URL
