import pytest
from fastapi import status


@pytest.mark.asyncio
async def test_shorten_and_redirect(test_client):
    # Create short URL
    resp = await test_client.post("/api/v1/shorten", json={"url": "https://google.com/"})
    assert resp.status_code == status.HTTP_200_OK
    data = resp.json()
    short_code = data["short_code"]

    # Stats check
    stats = await test_client.get(f"/api/v1/stats/{short_code}")
    assert stats.status_code == 200
    assert stats.json()["original_url"] == "https://google.com/"

    # Redirect
    redirect = await test_client.get(f"/api/v1/{short_code}", follow_redirects=False)
    assert redirect.status_code == status.HTTP_307_TEMPORARY_REDIRECT
    assert redirect.headers["location"] == "https://google.com/"
