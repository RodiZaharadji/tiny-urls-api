from importlib.machinery import SourceFileLoader
from importlib.util import spec_from_file_location, module_from_spec
from pathlib import Path

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError, NoResultFound

from tiny.common.exceptions_handlers import default_exception_handler, validation_exception_handler, \
    sqlalchemy_exception_handler, sqlalchemy_no_result_found_exception_handler


def create_app() -> FastAPI:
    app = FastAPI()
    register_routers(app)
    register_exception_handlers(app)

    return app


def register_routers(app: FastAPI):
    for path in map(str, Path("tiny").rglob("router.py")):
        spec = spec_from_file_location("module.name", path)
        module = module_from_spec(spec)
        spec.loader.exec_module(module)
        if router := getattr(module, "router", None):
            app.include_router(router)


def register_exception_handlers(app: FastAPI):
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(NoResultFound, sqlalchemy_no_result_found_exception_handler)
    app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)

    app.add_exception_handler(Exception, default_exception_handler)
