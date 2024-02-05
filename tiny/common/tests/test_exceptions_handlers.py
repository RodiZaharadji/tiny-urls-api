from unittest.mock import MagicMock

from asyncpg import UniqueViolationError, IntegrityConstraintViolationError
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import IntegrityError, NoResultFound
from starlette import status

from tiny.common.exceptions_handlers import default_exception_handler, validation_exception_handler, \
    sqlalchemy_exception_handler, sqlalchemy_no_result_found_exception_handler


class TestExceptionsHandlers:

    async def test_default_exception_handler(self, routes_test_client):
        response = await default_exception_handler(MagicMock(), Exception("Something"))

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR, response.body
        assert response.body == b'{"detail":"Something went wrong, please contact support"}'

    async def test_validation_exception_handler_400(self, routes_test_client):
        error = RequestValidationError(errors=[{"type": "value_error.missing"}])
        response = await validation_exception_handler(MagicMock(), error)

        assert response.status_code == status.HTTP_400_BAD_REQUEST, response.body
        assert response.body == b'{"detail":[{"type":"value_error.missing"}]}'

    async def test_validation_exception_handler_412(self, routes_test_client):
        error = RequestValidationError(errors=[{"type": "value_error.regex"}])
        response = await validation_exception_handler(MagicMock(), error)

        assert response.status_code == status.HTTP_412_PRECONDITION_FAILED, response.body
        assert response.body == b'{"detail":[{"type":"value_error.regex"}]}'

    async def test_sqlalchemy_exception_handler_409(self, routes_test_client):
        origin_error = MagicMock(__cause__=UniqueViolationError())
        error = IntegrityError(orig=origin_error, statement="", params={})
        response = await sqlalchemy_exception_handler(MagicMock(), error)

        assert response.status_code == status.HTTP_409_CONFLICT, response.body
        assert response.body == b'{"detail":"Item already exist"}'

    async def test_sqlalchemy_exception_handler_500(self, routes_test_client):
        origin_error = MagicMock(__cause__=IntegrityConstraintViolationError())
        error = IntegrityError(orig=origin_error, statement="", params={})
        response = await sqlalchemy_exception_handler(MagicMock(), error)

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR, response.body
        assert response.body == b'{"detail":"Something went wrong, please contact support"}'

    async def test_sqlalchemy_no_result_found_exception_handler(self, routes_test_client):
        response = await sqlalchemy_no_result_found_exception_handler(MagicMock(), NoResultFound())

        assert response.status_code == status.HTTP_404_NOT_FOUND, response.body
        assert response.body == b'{"detail":"Item not found"}'
