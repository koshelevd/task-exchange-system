from pydantic import BaseSettings


class Settings(BaseSettings):
    DEBUG: bool = True
    RELOAD: bool = True
    SERVER_HOST: str = "0.0.0.0"
    SERVER_PORT: int = 8002
    CORS_ORIGINS: str = "http://localhost:8002"
