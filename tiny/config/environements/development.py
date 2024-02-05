from .base import ApplicationEnvironment, Settings


class DevelopmentSettings(Settings):
    APP_ENVIRONMENT: str = ApplicationEnvironment.DEVELOPMENT.value
