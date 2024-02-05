import pytest
from sqlalchemy.exc import IntegrityError, NoResultFound

from tiny.shortcodes.schemas import ShortCodeCreateSchema
from tiny.shortcodes.services import ShortCodeService


class TestShortCodeService:
    async def test_create_ok(self):
        short_code_model = ShortCodeCreateSchema(url="https://acme.com", shortcode="acmetestservcice")
        short_code = await ShortCodeService.create(short_code_model)

        assert short_code.url == short_code_model.url
        assert short_code.shortcode == short_code_model.shortcode

    async def test_create_ok_autogenerate_shortcode(self):
        short_code_model = ShortCodeCreateSchema(url="https://acme.com")
        short_code = await ShortCodeService.create(short_code_model)

        assert short_code.url == short_code_model.url
        assert short_code.shortcode is not None

    async def test_create_ko(self):
        short_code_model = ShortCodeCreateSchema(url="https://acme.com", shortcode="acmetestservciceduplication")
        await ShortCodeService.create(short_code_model)

        with pytest.raises(IntegrityError):
            await ShortCodeService.create(short_code_model)

    async def test_get_ok(self):
        short_code_model = ShortCodeCreateSchema(url="https://acme.com", shortcode="acmetestservciceget")
        await ShortCodeService.create(short_code_model)

        short_code = await ShortCodeService.get(short_code_model.shortcode)

        assert short_code.url == short_code_model.url
        assert short_code.shortcode == short_code_model.shortcode

    async def test_get_ko(self):
        shortcode = "acmetestservcicegetko"

        with pytest.raises(NoResultFound):
            await ShortCodeService.get(shortcode)

    async def test_get_redirect_ok(self):
        short_code_model = ShortCodeCreateSchema(url="https://acme.com", shortcode="acmetestservcicegetredirect")
        initial_short_code = await ShortCodeService.create(short_code_model)

        requests_count = 3
        for _ in range(requests_count):
            redirect_url = await ShortCodeService.get_redirect(short_code_model.shortcode)
            assert redirect_url == short_code_model.url

        short_code = await ShortCodeService.get(short_code_model.shortcode)
        assert short_code.redirect_count == initial_short_code.redirect_count + requests_count

    async def test_get_redirect_ko(self):
        shortcode = "acmetestservcicegetredirectko"

        with pytest.raises(NoResultFound):
            await ShortCodeService.get_redirect(shortcode)
