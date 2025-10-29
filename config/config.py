import os
from dotenv import load_dotenv
from pathlib import Path

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

class Settings:
    # GENERAL
    PROJECT_NAME: str = "Ramon Test Board"
    PROJECT_VERSION: str = "1.0.0"

    # DATABASE
    POSTGRES_USER: str = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB")
    DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"

    # OAUTH2_JWT
    ACCESS_TOKEN_EXPIRES_IN: int = os.getenv("ACCESS_TOKEN_EXPIRES_IN")
    REFRESH_TOKEN_EXPIRES_IN: int = os.getenv("REFRESH_TOKEN_EXPIRES_IN")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM")
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = os.getenv("EMAIL_RESET_TOKEN_EXPIRE_HOURS")

settings = Settings()