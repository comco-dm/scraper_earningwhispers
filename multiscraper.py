from __future__ import annotations

import asyncio
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from typing import Dict, List

from scraper import fetch_earnings


def _fetch_single(date_str: str) -> Dict:
    """Synchronous helper to call the async fetcher inside a new event loop.

    Running ``aiohttp`` in a fresh loop per thread is safe and avoids loop sharing
    issues inside ``ThreadPoolExecutor``.
    """
    return asyncio.run(fetch_earnings(date_str))


def fetch_earnings_range(days: int = 30) -> List[Dict]:
    """Fetch earnings data for *today* and the next ``days`` − 1 days.

    Multithreaded to decrease total latency. Returns a list of dicts, each with
    keys ``date`` and ``data``.
    """
    tz = ZoneInfo("America/New_York")
    start = datetime.now(tz).date()
    date_strs = [(start + timedelta(days=i)).strftime("%Y%m%d") for i in range(days)]

    # Create a new executor for each call to avoid shutdown issues
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(_fetch_single, date_str) for date_str in date_strs]
        results = []
        for i, future in enumerate(futures):
            data = future.result()
            results.append({"date": date_strs[i], "data": data})

    return results 