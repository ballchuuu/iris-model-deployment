import aiohttp

class aioHttpClient:
    session = None

    @classmethod
    def start(self):
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=60)
        )

    @classmethod
    async def shutdown(self):
        if self.session is not None:
            await self.session.close()
            self.session = None