from __future__ import annotations

from datetime import datetime
from zoneinfo import ZoneInfo
import asyncio

from fastapi import FastAPI, Path

from scraper import fetch_earnings
from multiscraper import fetch_earnings_range

app = FastAPI(title="Earnings Whispers Scraper API")


@app.get("/")
async def root():
    """Return today's earnings calendar data automatically (US Eastern Time)."""
    today = datetime.now(ZoneInfo("America/New_York"))
    date_str = today.strftime("%Y%m%d")
    return await fetch_earnings(date_str)


@app.get("/scrape/{date}")
async def scrape(
    date: str = Path(
        ...,
        description="Date in YYYYMMDD format",
        example=datetime.now(ZoneInfo("America/New_York")).strftime("%Y%m%d")
    )
):
    """Return earnings-calendar JSON for the given ``YYYYMMDD`` date."""
    return await fetch_earnings(date)


@app.get("/scrape_next")
async def scrape_next(days: int = 30):
    """Return earnings data for today and the next ``days-1`` days (default 30).
    Computation runs in a thread pool to parallelise network I/O.
    """
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, fetch_earnings_range, days) 