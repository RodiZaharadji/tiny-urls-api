from fastapi import APIRouter
from starlette.responses import JSONResponse

router = APIRouter(prefix="/common", tags=["common"])


@router.get("/health")
async def get():
    return JSONResponse(
        {
            "status": "Ok",
        }
    )
