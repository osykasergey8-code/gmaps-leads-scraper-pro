
import os
from dotenv import load_dotenv
load_dotenv()
OUTPUT = os.getenv("OUTPUT", "data/gmaps_leads.csv")
HEADLESS = False