# 🚀 GMaps Leads Scraper Pro

![Banner](assets/banner.png)

[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Playwright](https://img.shields.io/badge/Playwright-45ba4b?style=for-the-badge&logo=playwright&logoColor=white)](https://playwright.dev)
[![License MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![No API Key](https://img.shields.io/badge/No%20API%20Key-Required-success?style=for-the-badge)](#)

> **Professional Google Maps Business Scraper** - Automated lead extraction with anti-bot bypass, smart scrolling, and styled Excel export. No API key needed.

### ✨ Demo

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

### 📊 Result - Professional Excel Export

| Business Name | Rating | Phone | Verified |
|---------------|--------|-------|----------|
| Pellico 3 Milano | 4.9 ⭐ | 02 8821 1234 | Yes |
| Mercato Centrale Milano | 4.4 ⭐ | 02 3792 8400 | Yes |
| Trippa | 4.6 ⭐ | 327 668 7908 | Yes |

*Clean CSV + Styled XLSX with auto-filter, freeze pane, color-coded ratings (4.6+ green)*

---

### 🔥 Features

- ✅ **Fixed 0 Cards Bug** - Uses `div[role="feed"] > div > div[jsaction] > a.hfpxzc` instead of outdated `div[role="article"]`
- ✅ **Smart Scroll** - Scrolls inside results panel, not whole page
- ✅ **Cookie Auto-Handling** - Works in EU (Accetta tutto / Accept all)
- ✅ **Anti-Bot Bypass** - Custom User-Agent + disable automation flag
- ✅ **Professional Export** - Clean phones, stripped UTM URLs, sorted by rating
- ✅ **Permission Safe** - No crash if CSV open in Excel

### 📁 Project Structure
```
gmaps-leads-scraper-pro/
├── src/
│   ├── scraper.py      # Playwright scraper - fixed selectors 2026
│   ├── exporter.py     # Pro exporter - CSV + styled Excel
│   ├── verifier.py     # Phone & website verification
│   ├── config.py       # Env config
│   └── utils.py
├── data/
│   ├── gmaps_leads.csv
│   └── gmaps_leads_PRO.xlsx
├── main.py
└── requirements.txt
```

### 🚀 Quick Start

```bash
# 1. Clone
git clone https://github.com/osykasergey8-code/gmaps-leads-scraper-pro.git
cd gmaps-leads-scraper-pro

# 2. Install
pip install -r requirements.txt
playwright install chromium

# 3. Run (visible browser for debug)
# in src/config.py set HEADLESS=False
python main.py --query "restaurants in Milan" --max 50

# 4. Headless pro run
# in src/config.py set HEADLESS=True
python main.py --query "dentists in Berlin" --max 100 --output data/berlin.csv
```

### 🛠️ Tech Stack

- **Python 3.10+**
- **Playwright** - browser automation
- **Pandas + OpenPyXL** - data + pro Excel styling

### 📦 Requirements

```
playwright>=1.44.0
pandas>=2.2.3
python-dotenv>=1.0.1
openpyxl>=3.1.2
```

### 🐛 What was fixed (v2)

**Before:** `Found 0 cards` due to outdated selector
**After:** 34 cards found, 20 leads with phones

1. Selector: `div[role="article"]` → `a.hfpxzc` with `/maps/place/` filter
2. Scroll: `window.scroll` → `feed.scrollBy(0, 2500)`
3. Extraction: Icon chars `` cleaned, tel: links parsed

### 📄 License

MIT - free for commercial use.

### 👨‍💻 Author

**Sergey Osyka** - [GitHub](https://github.com/osykasergey8-code) | Upwork Profile

> Built for lead generation, local business research, and sales prospecting.

---
⭐ Star this repo if it helped you scrape leads!
