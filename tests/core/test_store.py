import pytest
from app.core.aiohttp.client import aioHttpClient
from app.core.store import Store

@pytest.mark.asyncio
async def test_store():
    store = Store()
    assert isinstance(store.bento_client, aioHttpClient)

    store.start()
    assert store.bento_client.session is not None

    await store.shutdown()
    assert store.bento_client.session is None
