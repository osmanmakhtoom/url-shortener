from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db_dependency
from app.schemas import ShortenRequest, ShortenResponse
from app.services import URLService

router = APIRouter()


@router.post("/shorten", response_model=ShortenResponse)
async def create_short(
    payload: ShortenRequest, session: AsyncSession = Depends(get_db_dependency)
) -> ShortenResponse:
    us = URLService(session)
    url = await us.create_short(str(payload.url))
    return ShortenResponse(
        short_code=url.short_code,
        original_url=url.original_url,
        short_url=f"/{url.short_code}",
        created_at=url.created_at.isoformat(),
    )
