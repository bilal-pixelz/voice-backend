from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    ENVIRONMENT: str = "development"
    DATABASE_URL: str
    JWT_SECRET_KEY: str
    OPENAI_API_KEY: str
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    CORS_ORIGINS: str = "http://localhost:3000"
    GOOGLE_FRONTEND_REDIRECT_URI: list = ["http://localhost:3000/google/callback"]

    class Config:
        env_file = ".env"

settings = Settings()