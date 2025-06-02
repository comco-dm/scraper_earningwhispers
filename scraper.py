from __future__ import annotations

import aiohttp

from context import cookies, headers, url_target


async def fetch_earnings(date: str) -> dict:
    """Fetch earnings-calendar JSON for the given YYYYMMDD date.

    This is kept tiny by delegating error handling to the caller and by
    avoiding side-effects. HTTP errors propagate via ``aiohttp.ClientResponseError``.
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{url_target}/{date}", cookies=cookies, headers=headers) as response:
            response.raise_for_status()
            return await response.json() 