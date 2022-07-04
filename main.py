#####
# Indie Cinema Scraper
# v1.1
# May 27, 2022
# Paul Jarvey
######

# All dependencies
# from urllib.request import urlopen, Request
# from urllib.parse import urlparse
# from bs4 import BeautifulSoup as Soup
# import re
# import json
# import datetime
# from scrapers.scrapingTools import requestandparse, checkurl

# import modules
import pandas as pd
from pathlib import Path

# link files
from scrapers import cinescrape_01_Cinesphere
from scrapers import cinescrape_02_TIFFBellLightbox
from scrapers import cinescrape_03_Cineplex
from scrapers import cinescrape_04_TIFFDigital
from scrapers import cinescrape_05_theRevue
from scrapers import cinescrape_06_theFox

# Load data or init if none exists
if not Path('listings.csv').is_file():
    listings = pd.DataFrame(columns=['timestamp', 'cinema', 'mTitle', 'mTime', 'mURL', 'mPosterURL'])
    print("Historical data not found, initiating new...")
else:
    listings = pd.read_csv('listings.csv')
    print("Restoring from CSV...")

cinemas = pd.read_csv('cinemas.csv')

# Scrapers

# scrape cineplex 1 (note needs cinema location ID values)

print("Beginning scrape...")
listings01 = cinescrape_01_Cinesphere.scrape_01_cinesphere(0)
listings02 = cinescrape_02_TIFFBellLightbox.scrape_02_cineplex(1)
listings03 = cinescrape_03_Cineplex.scrape_03_cineplex(2, 7130)
listings04 = cinescrape_03_Cineplex.scrape_03_cineplex(3, 7199)
listings05 = cinescrape_03_Cineplex.scrape_03_cineplex(4, 7400)
listings06 = cinescrape_03_Cineplex.scrape_03_cineplex(5, 7293)
listings07 = cinescrape_03_Cineplex.scrape_03_cineplex(6, 7139)
listings08 = cinescrape_03_Cineplex.scrape_03_cineplex(7, 7406)
listings09 = cinescrape_03_Cineplex.scrape_03_cineplex(8, 7298)
listings10 = cinescrape_03_Cineplex.scrape_03_cineplex(9, 7402)
listings11 = cinescrape_03_Cineplex.scrape_03_cineplex(10, 7115)
listings12 = cinescrape_03_Cineplex.scrape_03_cineplex(11, 7253)
listings13 = cinescrape_04_TIFFDigital.scrape_02_cineplex(12)
listings14 = cinescrape_05_theRevue.scrape_05_therevue(13)
listings15 = cinescrape_06_theFox.scrape_06_thefox(14)

# todo: add remaining scrapers
# todo: wrap scrapers in a try

# list all listings results
frames = [listings,
          listings01,
          listings02,
          listings03]
print("collecting results...")

# concatenate listings dataframes
listingsOutput = pd.concat(frames)
print("Total listings gathered: "+str(len(listingsOutput)))

# remove all dates on past dates
listingsOutput = listingsOutput[pd.to_datetime(listingsOutput['mTime']) >= pd.to_datetime("today")]
print("Total listings in the future: "+str(len(listingsOutput)))

# dedupe
listingsOutput = pd.DataFrame.drop_duplicates(listingsOutput, subset=["cinema", "mTitle", "mTime"])
print("Total unique future listings: "+str(len(listingsOutput)))

print("Summary: ")
listingsOutput.groupby(['cinema']).count()

# save as CSV
listings.to_csv('listings.csv', index=False)
print("Results saved.")
