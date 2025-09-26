from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import RedirectResponse

from app.core.db import get_db_dependency
from app.decorators import log_visit
from app.services import URLService

router = APIRouter()


@router.get("/{short_code}")
@log_visit("short_code")
async def redirect_short(
    short_code: str,
    request: Request,
    session: AsyncSession = Depends(get_db_dependency),
) -> RedirectResponse:
    us = URLService(session)
    url = await us.get_by_code(short_code)
    if not url:
        raise HTTPException(status_code=404, detail="Not found")
    return RedirectResponse(url.original_url, status_code=307)
