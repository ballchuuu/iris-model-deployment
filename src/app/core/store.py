from app.core.aiohttp.client import aioHttpClient

class Store:
    bento_client: aioHttpClient = aioHttpClient()

    def start(self):
        self.bento_client.start()

    async def shutdown(self):
        await self.bento_client.shutdown()

store = Store()