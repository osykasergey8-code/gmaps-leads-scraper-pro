# Google Maps Business Leads Scraper

Python + Playwright scraper that turns a Google Maps search ("Restaurants in Milano") into a clean, de-duplicated list of business leads, ready for a CRM or cold outreach. No API key needed.

**Output columns:** Business Name, Address, Phone, Website, Category, Rating, Verified

A sample result is in [`sample_leads_milan.csv`](sample_leads_milan.csv) and a styled Excel version in [`PRO-Excel.xlsx`](PRO-Excel.xlsx).

## Features

- Real browser automation (Playwright, Chromium) with automatic cookie-banner handling
- Smart scrolling through the results feed, then opens each business card for full details
- Fallback selectors, so small Google Maps layout changes do not break the run
- Phone and website cleaning and verification, de-duplication by name and address
- Export to CSV (and styled Excel)

## Project structure

```
main.py            command line entry point
src/scraper.py     Playwright: search, scroll, open cards, extract fields
src/verifier.py    phone / website cleaning and verification
src/exporter.py    de-duplication and CSV / Excel export
src/config.py      settings (output path, headless mode via .env)
src/utils.py       logging helper
```

## Quick start

```bash
pip install -r requirements.txt
playwright install chromium
python main.py --query "Restaurants in Milano" --max 100 --output data/gmaps_leads.csv
```

| Option | Meaning |
|---|---|
| `--query` | What to search, e.g. `"Dentists in Roma"` |
| `--max` | Maximum number of businesses to collect (default 50) |
| `--output` | Output file (default `data/gmaps_leads.csv`) |

Settings can be overridden in a `.env` file (`OUTPUT=...`).

## Stack

Python, Playwright, pandas, openpyxl, python-dotenv

## Notes

Collect only publicly listed business information and respect the terms of the services you scrape. Need a custom lead list or scraper? Contact me via my [Contra profile](https://contra.com/sergey_osyka_lw5bxb5o).
