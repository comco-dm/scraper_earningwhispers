from __future__ import annotations

from datetime import datetime
from zoneinfo import ZoneInfo

from fastapi import FastAPI, Path

from scraper import fetch_earnings

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