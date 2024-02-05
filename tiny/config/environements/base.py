from enum import Enum
from pathlib import Path
from pydantic import BaseSettings, Field, PostgresDsn, AnyUrl, constr

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent


class ApplicationEnvironment(Enum):
    TESTING = "testing"
    DEVELOPMENT = "development"


class Settings(BaseSettings):
    # Env config
    APP_ENVIRONMENT: str = Field(...)
    RELEASE: str | None
    SUPPORT_EMAIL: str = "support@tiny.com"
    BASE_DOMAIN: AnyUrl = "http://localhost"

    # SQLAlchemy config
    SQLALCHEMY_DATABASE_URI: PostgresDsn
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    SQLALCHEMY_ECHO: bool | str = False

    class Config:
        env_file = BASE_DIR / ".env"
