# Earnings Whispers Scraper API

A FastAPI service that scrapes earnings calendar data from Earnings Whispers.

## 🚀 Live Service

**API URL**: https://earnings-scraper-870495329690.us-central1.run.app

## 📡 Endpoints

- `GET /` - Welcome message
- `GET /scrape/{YYYYMMDD}` - Get earnings data for specific date

## 🔄 Auto-Deployment

This service automatically deploys when pushing to the `main` branch via Cloud Build.

## 🧪 Example Usage

```bash
# Get earnings for June 5, 2025
curl "https://earnings-scraper-870495329690.us-central1.run.app/scrape/20250605" | jq
``` 