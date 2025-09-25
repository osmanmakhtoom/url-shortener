import asyncio
import json
import pytest
from app.core.cache import redis_client


@pytest.mark.asyncio
async def test_redis_set_get_delete():
    await redis_client.set("foo", "bar")
    val = await redis_client.get("foo")
    assert val == "bar"
    await redis_client.delete("foo")
    assert await redis_client.get("foo") is None


@pytest.mark.asyncio
async def test_rabbitmq_publish_consume(rabbitmq_client_fixture):
    messages = []

    async def handler(msg):
        payload = json.loads(msg.decode("utf-8"))
        messages.append(payload)

    consume_task = asyncio.create_task(rabbitmq_client_fixture.consume("test_queue", handler))

    await rabbitmq_client_fixture.publish("test_queue", {"hello": "world"})

    await asyncio.sleep(0.5)

    consume_task.cancel()
    try:
        await consume_task
    except asyncio.CancelledError:
        pass

    assert messages, "No messages consumed"
    assert messages[0]["hello"] == "world"
