from .base import ApplicationEnvironment, Settings


class TestingSettings(Settings):
    APP_ENVIRONMENT: str = ApplicationEnvironment.TESTING.value