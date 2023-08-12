from pydantic import BaseSettings


class Settings(BaseSettings):
    DEBUG: bool = True
    RELOAD: bool = True
    SERVER_HOST: str = "0.0.0.0"
    SERVER_PORT: int = 8001
    CORS_ORIGINS: str = "http://localhost:8001"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 3000
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    ALGORITHM: str = "HS256"
    JWT_SECRET_KEY: str = "secret"
    JWT_REFRESH_SECRET_KEY: str = "secret"


app_settings = Settings()
