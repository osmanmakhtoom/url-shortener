import pytest
from app.services import URLService, VisitService
from app.models import URL


@pytest.mark.asyncio
async def test_create_short_and_get(db_session):
    us = URLService(db_session)
    url = await us.create_short("https://example.com")
    assert isinstance(url, URL)
    assert url.short_code

    fetched = await us.get_by_code(url.short_code)
    assert fetched.original_url == "https://example.com"
