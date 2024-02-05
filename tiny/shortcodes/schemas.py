from typing import Optional

from pydantic import BaseModel, AnyHttpUrl, Field
from pydantic.schema import datetime


class ShortCodeCreateSchema(BaseModel):
    url: AnyHttpUrl
    shortcode: Optional[str] = Field(
        min_length=6, regex=r"^[a-zA-Z0-9_]*$"
    )


class ShortCodeSchema(BaseModel):
    shortcode: str

    class Config:
        orm_mode = True


class ShortCodeStatusSchema(BaseModel):
    created: datetime
    lastRedirect: datetime
    redirectCount: int

    class Config:
        orm_mode = True
