# Earnings Whispers Scraper API

A FastAPI service that scrapes earnings calendar data from Earnings Whispers.

## 🚀 Live Service

**API URL**: https://earnings-scraper-870495329690.us-central1.run.app

## 📡 Endpoints

- `GET /` - **Automatically returns today's earnings data** (US Eastern Time)
- `GET /scrape/{YYYYMMDD}` - Get earnings data for specific date

## 🔄 Auto-Deployment

This service automatically deploys when pushing to the `main` branch via Cloud Build.

## 🧪 Example Usage

```bash
# Get today's earnings automatically
curl "https://earnings-scraper-870495329690.us-central1.run.app/" | jq

# Get earnings for specific date (June 5, 2025)
curl "https://earnings-scraper-870495329690.us-central1.run.app/scrape/20250605" | jq
```

## 📊 Response Format

Both endpoints return the raw JSON array from Earnings Whispers:
```json
[
  {
    "ticker": "AVGO",
    "company": "Broadcom Inc.",
    "total": 128,
    "nextEPSDate": "2025-06-05T00:00:00",
    "releaseTime": 3,
    "qDate": "4/2025",
    "q1RevEst": 14920000000.0,
    "q1EstEPS": 1.58,
    "confirmDate": "2025-05-05T08:11:11.087",
    "epsTime": "2025-03-06T16:15:00",
    "quarterDate": "2025-04-30T00:00:00",
    "qSales": 12487.0
  }
]
``` 