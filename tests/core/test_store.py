import pytest

from app.core.store import Store
from app.core.aiohttp.client import aioHttpClient

@pytest.mark.asyncio
async def test_store():
    store = Store()
    assert isinstance(store.bento_client, aioHttpClient)

    store.start()
    assert store.bento_client.session is not None

    await store.shutdown()
    assert store.bento_client.session is None
