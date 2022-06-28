#####
# Indie Cinema Scraper
# v1.1
# May 27 2022
# Paul Jarvey
######

# load libraries
from urllib.request import urlopen, Request
from urllib.parse import urlparse
from bs4 import BeautifulSoup as Soup
import pandas as pd
import re
import time
from datetime import datetime
from pathlib import Path

# link files
from scrapers import cinescrape_01_cineplex
from scrapers.scrapingTools import checkurl
from scrapers.scrapingTools import requestandparse

cinescrape_01_cineplex.scrape_01_cineplex(2,7130)

# Load data or init if none exists
if not Path('listings.csv').is_file():
    listings = pd.DataFrame(columns=['timestamp', 'cinema', 'mTitle', 'mTime', 'mURL', 'mPosterURL'])
    print("Historical data not found, initiating new...")
else:
    listings = pd.read_csv('listings.csv')
    print("Restoring from CSV...")

cinemas = pd.read_csv('cinemas.csv')


# format URLS
def checkurl(requested_url):
    if not urlparse(requested_url).scheme:
        requested_url = "https://" + requested_url
    return requested_url


# Set agent and request date
def requestandparse(requested_url):
    requested_url = checkurl(requested_url)
    try:
        # define headers to be provided for request authentication
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) ' 
                   'AppleWebKit/537.11 (KHTML, like Gecko) '
                   'Chrome/23.0.1271.64 Safari/537.11',
                   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                   'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                   'Accept-Encoding': 'none',
                   'Accept-Language': 'en-US,en;q=0.8',
                   'Connection': 'keep-alive'}
        request_obj = Request(url=requested_url, headers=headers)
        opened_url = urlopen(request_obj)
        page_html = opened_url.read()
        opened_url.close()
        page_soup = Soup(page_html, "html.parser")
        return page_soup, requested_url

    except Exception as e:
        print(e)



listings.to_csv('listings.csv', index=False)




