import pytest
from starlette import status

from tiny.shortcodes.schemas import ShortCodeCreateSchema
from tiny.shortcodes.services import ShortCodeService


class TestShourtcodesRouter:

    @pytest.mark.parametrize(
        "request_body",
        [
            {"url": "https://tiny.com"},
            {"url": "https://tiny.com", "shortcode": "testshortcode"},
        ]
    )
    async def test_create_shortcode_ok(self, routes_test_client, request_body):
        response = await routes_test_client.post(
            "/shorten", json=request_body
        )

        assert response.status_code == status.HTTP_201_CREATED, response.content
        assert response.json()["shortcode"] is not None

    @pytest.mark.parametrize(
        "request_body",
        [
            {"url": "invalid_url"},
            {"url": "https://tiny.com", "shortcode": "invsh"},
        ]
    )
    async def test_create_shortcode_ko_412(self, routes_test_client, request_body):
        response = await routes_test_client.post(
            "/shorten", json=request_body
        )

        assert response.status_code == status.HTTP_412_PRECONDITION_FAILED, response.content

    async def test_create_shortcode_ko_400(self, routes_test_client):
        response = await routes_test_client.post(
            "/shorten", json={}
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST, response.content

    async def test_create_shortcode_ko_shortcode_already_in_use(self, routes_test_client):
        short_code = await ShortCodeService.create(
            ShortCodeCreateSchema(url="https://acme.com", shortcode="acmetestalreadyexists")
        )
        response = await routes_test_client.post(
            "/shorten", json={"url": "https://acme2.com", "shortcode": short_code.shortcode}
        )

        assert response.status_code == status.HTTP_409_CONFLICT, response.content

    async def test_get_shortcode_ok(self, routes_test_client):
        short_code = await ShortCodeService.create(ShortCodeCreateSchema(url="https://acme.com", shortcode="acmetest"))
        response = await routes_test_client.get(
            f"/{short_code.shortcode}"
        )

        assert response.status_code == status.HTTP_302_FOUND, response.content
        assert response.headers["location"] == short_code.url

    async def test_get_shortcode_ko_not_found(self, routes_test_client):
        response = await routes_test_client.get(
            f"/invalid_short_code"
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND, response.content

    async def test_get_shortcode_status_ok(self, routes_test_client):
        short_code = await ShortCodeService.create(
            ShortCodeCreateSchema(url="https://acme.com", shortcode="acmeteststatus")
        )
        response = await routes_test_client.get(
            f"/{short_code.shortcode}/status"
        )

        assert response.status_code == status.HTTP_200_OK, response.content
        assert response.json() == {
            "created": short_code.created_at.isoformat(),
            "lastRedirect": short_code.updated_at.isoformat(),
            "redirectCount": short_code.redirect_count
        }

    async def test_get_shortcode_status_ok_not_found(self, routes_test_client):
        response = await routes_test_client.get(
            f"/invalid_short_code/status"
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND, response.content
