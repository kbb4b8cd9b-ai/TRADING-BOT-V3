import os
import base64
import httpx

class Trading212Adapter:
    def __init__(self, live=False):
        self.live = live
        self.base_url = (
            "https://live.trading212.com/api/v0"
            if live else "https://demo.trading212.com/api/v0"
        )
        self.api_key = os.getenv("T212_API_KEY")
        self.api_secret = os.getenv("T212_API_SECRET")

    def headers(self):
        if not self.api_key or not self.api_secret:
            raise RuntimeError("Trading 212 credentials are not configured.")
        raw = f"{self.api_key}:{self.api_secret}".encode()
        token = base64.b64encode(raw).decode()
        return {"Authorization": f"Basic {token}"}

    async def account(self):
        async with httpx.AsyncClient(timeout=15) as client:
            r = await client.get(
                f"{self.base_url}/equity/account/summary",
                headers=self.headers()
            )
            r.raise_for_status()
            return r.json()

    async def positions(self):
        async with httpx.AsyncClient(timeout=15) as client:
            r = await client.get(
                f"{self.base_url}/equity/positions",
                headers=self.headers()
            )
            r.raise_for_status()
            return r.json()

    async def market_order(self, symbol, side, quantity):
        # Deliberately disabled in final starter build.
        raise RuntimeError(
            "Live order execution is disabled. Validate paper trading, risk controls and broker setup first."
        )

    async def cancel_order(self, order_id):
        raise RuntimeError("Live execution is disabled in this build.")
