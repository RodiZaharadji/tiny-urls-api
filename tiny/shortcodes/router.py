from fastapi import APIRouter
from starlette import status
from starlette.responses import JSONResponse, RedirectResponse

from tiny.shortcodes.models import ShortCode
from tiny.shortcodes.schemas import ShortCodeCreateSchema, ShortCodeSchema, ShortCodeStatusSchema
from tiny.shortcodes.services import ShortCodeService

router = APIRouter(prefix="", tags=["shortcodes"])


@router.post("/shorten", status_code=status.HTTP_201_CREATED, response_model=ShortCodeSchema)
async def create_shortcode(payload: ShortCodeCreateSchema):
    return await ShortCodeService.create(payload)


@router.get("/{shortcode}/status", status_code=status.HTTP_200_OK, response_model=ShortCodeStatusSchema)
async def get_status(shortcode: str):
    short_code: ShortCode = await ShortCodeService.get(shortcode=shortcode)
    return {
        "created": short_code.created_at,
        "lastRedirect": short_code.updated_at,
        "redirectCount": short_code.redirect_count
    }


@router.get("/{shortcode}", status_code=status.HTTP_302_FOUND)
async def get_shortcode(shortcode: str):
    redirect_url: str = await ShortCodeService.get_redirect(shortcode=shortcode)
    return RedirectResponse(url=redirect_url, status_code=status.HTTP_302_FOUND)

