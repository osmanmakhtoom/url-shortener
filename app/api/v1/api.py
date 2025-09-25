from fastapi import APIRouter
from app.api.v1.endpoints import create_short, get_stats, redirect_short

api_router = APIRouter()

api_router.include_router(create_short.router, tags=["shorten"])
api_router.include_router(get_stats.router, tags=["stats"])
api_router.include_router(redirect_short.router, tags=["redirect"])
