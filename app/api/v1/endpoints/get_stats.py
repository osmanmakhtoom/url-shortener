from fastapi import APIRouter, Depends, HTTPException
from pydantic import HttpUrl
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db_dependency
from app.schemas import StatsResponse
from app.services import URLService

router = APIRouter()


@router.get("/stats/{short_code}", response_model=StatsResponse)
async def get_stats(
    short_code: str, session: AsyncSession = Depends(get_db_dependency)
) -> StatsResponse:
    us = URLService(session)
    url = await us.get_by_code(short_code)
    if not url:
        raise HTTPException(status_code=404, detail="Not found")
    return StatsResponse(
        original_url=HttpUrl(url.original_url),
        short_code=url.short_code,
        visit_count=url.visit_count,
        created_at=url.created_at,
    )
