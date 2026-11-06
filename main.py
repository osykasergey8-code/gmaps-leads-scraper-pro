
import argparse
from src.scraper import GMapsScraper
from src.exporter import export_leads
from src.config import OUTPUT, HEADLESS

def main():
    parser = argparse.ArgumentParser(description="GMaps Leads Scraper Pro")
    parser.add_argument("--query", required=True, help='e.g. "Restaurants in Milano"')
    parser.add_argument("--max", type=int, default=50)
    parser.add_argument("--output", default=OUTPUT)
    args = parser.parse_args()

    scraper = GMapsScraper(headless=HEADLESS)
    leads = scraper.scrape(args.query, max_results=args.max)
    export_leads(leads, args.output)

if __name__ == "__main__":
    main()
