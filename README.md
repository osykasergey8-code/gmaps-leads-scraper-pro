# 🚀 GMaps Leads Scraper Pro

[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Playwright](https://img.shields.io/badge/Playwright-45ba4b?style=for-the-badge&logo=playwright&logoColor=white)](https://playwright.dev)
[![License MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![No API Key](https://img.shields.io/badge/No%20API%20Key-Required-success?style=for-the-badge)](#)

> **Professional Google Maps business scraper.** Turns a Google Maps search ("Restaurants in Milano") into a clean, de-duplicated list of business leads, exported to CSV and styled Excel. No API key needed.

**Output columns:** Business Name, Address, Phone, Website, Category, Rating, Verified

A sample result is in [`sample_leads_milan.csv`](sample_leads_milan.csv) and a styled Excel version in [`PRO-Excel.xlsx`](PRO-Excel.xlsx).

## Demo

```
🔍 Searching Google Maps: restaurants in Milan
✅ Feed panel found
✅ Scroll 1: ~18 cards | Scroll 2: ~21 cards | Scroll 3: ~28 cards
✅ Found 34 valid business cards

1/20 -> Mercato Centrale Milano | Phone: 02 3792 8400 | Addr: Via Giovanni Battista...
2/20 -> Ristorante Galleria | Phone: 02 8646 4912 | Rating: 4.5
...
✅ Exported 20 leads to data/gmaps_leads.csv
✅ Professional Excel saved to data/gmaps_leads_PRO.xlsx
```

Excel export: auto-filter, frozen header row, colour-coded ratings (4.6+ green).

## Features

- **Smart scroll**: scrolls inside the results panel, not the whole page
- **Resilient selectors**: `div[role="feed"] > div > div[jsaction] > a.hfpxzc` with a `/maps/place/` filter and fallbacks
- **Cookie banner handling**: works in the EU ("Accetta tutto" / "Accept all")
- **Browser fingerprint hygiene**: custom User-Agent, automation flag disabled
- **Clean export**: normalized phones, stripped UTM parameters, de-duplication by name and address, sorted by rating
- **Safe to rerun**: does not crash if the CSV is open in Excel

## Project structure

```
main.py            command line entry point
src/scraper.py     Playwright: search, scroll, open cards, extract fields
src/verifier.py    phone / website cleaning and verification
src/exporter.py    de-duplication, CSV and styled Excel export
src/config.py      settings (output path, headless mode)
src/utils.py       logging helper
```

## Quick start

```bash
git clone https://github.com/osykasergey8-code/gmaps-leads-scraper-pro.git
cd gmaps-leads-scraper-pro
pip install -r requirements.txt
playwright install chromium

python main.py --query "restaurants in Milan" --max 50
python main.py --query "dentists in Berlin" --max 100 --output data/berlin.csv
```

| Option | Meaning |
|---|---|
| `--query` | What to search, e.g. `"Dentists in Roma"` |
| `--max` | Maximum number of businesses (default 50) |
| `--output` | Output CSV (default `data/gmaps_leads.csv`); the Excel file is saved next to it as `*_PRO.xlsx` |

The browser window is visible by default (`HEADLESS = False` in `src/config.py`). Set it to `True` for headless runs.

## Stack

Python 3.10+, Playwright, pandas, openpyxl, python-dotenv

## Notes

Collect only publicly listed business information and respect the terms of the services you scrape.

## License

MIT, free for commercial use.

## Author

**Sergey Osyka**: [GitHub](https://github.com/osykasergey8-code) | [Contra](https://contra.com/sergey_osyka_lw5bxb5o). Need a custom lead list or scraper? Get in touch via Contra.
