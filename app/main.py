from __future__ import annotations

from fastapi import FastAPI, HTTPException

from scraper import fetch_earnings

app = FastAPI(title="Earnings Whispers Scraper API")


@app.get("/scrape/{date}")
async def scrape(date: str):
    """Return earnings-calendar JSON for the given ``YYYYMMDD`` date."""
    try:
        return await fetch_earnings(date)
    except Exception as exc:  # noqa: BLE001  # propagate unexpected errors with context
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@app.get("/")
async def root():
    return {"message": "Welcome to the Earnings Whispers Scraper API"} 