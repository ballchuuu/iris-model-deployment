import pytest 

from app.core.aiohttp.client import aioHttpClient

@pytest.mark.asyncio
async def test_client():
    client = aioHttpClient()

    client.start()
    assert client.session is not None

    await client.shutdown()
    assert client.session is None