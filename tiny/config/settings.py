import os
from functools import lru_cache
from typing import Dict, Any

from .environements.base import ApplicationEnvironment, Settings
from .environements.development import DevelopmentSettings
from .environements.testing import TestingSettings

_environment_settings: Dict[Any, Any] = {
    ApplicationEnvironment.DEVELOPMENT.value: DevelopmentSettings,
    ApplicationEnvironment.TESTING.value: TestingSettings,
}


def _get_environment() -> str:
    app_environment = os.environ.get("APP_ENVIRONMENT", ApplicationEnvironment.DEVELOPMENT.value)
    if app_environment not in ApplicationEnvironment._value2member_map_:
        raise ValueError(f"Unknown {app_environment} environment.")
    return app_environment


@lru_cache
def get_settings() -> Settings:
    environment: str = _get_environment()
    return _environment_settings[environment]()
