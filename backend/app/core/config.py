from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    PROJECT_NAME: str = "Pink Wheels API"
    ENVIRONMENT: str = "development"

    DATABASE_URL: str = "postgresql+psycopg://pinkwheels:pinkwheels@localhost:5432/pink_wheels"

    JWT_SECRET: str = "change-me-in-production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    FRONTEND_URL: str = "http://localhost:5173"
    BACKEND_URL: str = "http://localhost:8000"

    OTP_PROVIDER_API_KEY: str = ""
    OTP_EXPIRY_MINUTES: int = 5
    OTP_MAX_ATTEMPTS: int = 5

    CORS_ORIGINS: str = "http://localhost:5173,http://localhost:5174"


settings = Settings()
