import traceback

from asyncpg import UniqueViolationError
from fastapi import Request
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError, NoResultFound
from starlette import status
from starlette.responses import JSONResponse


async def default_exception_handler(request: Request, exc: Exception):
    traceback.print_exc()

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Something went wrong, please contact support"},
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    traceback.print_exc()

    if any(error['type'] == 'value_error.missing' for error in exc.errors()):
        status_code = status.HTTP_400_BAD_REQUEST
    else:
        status_code = status.HTTP_412_PRECONDITION_FAILED

    return JSONResponse(
        status_code=status_code,
        content={"detail": exc.errors()},
    )


async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    if isinstance(getattr(getattr(exc, "orig", None), "__cause__", None), UniqueViolationError):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"detail": "Item already exist"},
        )

    return await default_exception_handler(request, exc)


async def sqlalchemy_no_result_found_exception_handler(request: Request, exc: NoResultFound):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": "Item not found"},
    )

