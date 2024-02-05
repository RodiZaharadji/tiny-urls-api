from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from tiny.config.environements.base import Settings, ApplicationEnvironment


def register_middlewares(app: FastAPI, settings: Settings):
    allow_origin_mapping = {
        ApplicationEnvironment.TESTING.value: r".*",
        ApplicationEnvironment.DEVELOPMENT.value: r".*",
    }
    app.add_middleware(
        CORSMiddleware,
        allow_origin_regex=allow_origin_mapping[settings.APP_ENVIRONMENT],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
