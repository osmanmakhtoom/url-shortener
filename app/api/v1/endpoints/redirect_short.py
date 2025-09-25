from starlette.responses import RedirectResponse
from fastapi import APIRouter, HTTPException, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_db_dependency
from app.services import URLService
from app.decorators import log_visit

router = APIRouter()


@router.get("/{short_code}")
@log_visit("short_code")
async def redirect_short(
    short_code: str,
    request: Request,
    session: AsyncSession = Depends(get_db_dependency),
):
    us = URLService(session)
    url = await us.get_by_code(short_code)
    if not url:
        raise HTTPException(status_code=404, detail="Not found")
    return RedirectResponse(url.original_url, status_code=307)
