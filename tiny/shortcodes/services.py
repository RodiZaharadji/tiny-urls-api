from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from tiny.database import use_session
from tiny.shortcodes.models import ShortCode
from tiny.shortcodes.schemas import ShortCodeCreateSchema


class ShortCodeService:
    @classmethod
    @use_session()
    async def create(cls, short_code_model: ShortCodeCreateSchema, session: AsyncSession) -> ShortCode:
        async with session.begin():
            instance = ShortCode(
                url=short_code_model.url,
                shortcode=short_code_model.shortcode,
            )

            session.add(instance)

        return instance

    @classmethod
    @use_session()
    async def get(cls, shortcode: str, session: AsyncSession) -> ShortCode:
        async with session.begin():
            instance = (await session.execute(
                select(ShortCode).where(ShortCode.shortcode == shortcode)
            )).scalar_one()

        return instance

    @classmethod
    @use_session()
    async def get_redirect(cls, shortcode: str, session: AsyncSession) -> str:
        async with session.begin():
            instance_url = (await session.execute(
                update(ShortCode).
                where(ShortCode.shortcode == shortcode).
                values(redirect_count=ShortCode.redirect_count + 1).
                returning(ShortCode.url)
            )).scalar_one()

        return instance_url
