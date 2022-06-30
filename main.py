#####
# Indie Cinema Scraper
# v1.1
# May 27, 2022
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
from scrapers import cinescrape_01_Cinesphere
from scrapers import cinescrape_02_TIFFBellLightbox
from scrapers import cinescrape_03_Cineplex
from scrapers import cinescrape_04_TIFFDigital

# Load data or init if none exists
if not Path('listings.csv').is_file():
    listings = pd.DataFrame(columns=['timestamp', 'cinema', 'mTitle', 'mTime', 'mURL', 'mPosterURL'])
    print("Historical data not found, initiating new...")
else:
    listings = pd.read_csv('listings.csv')
    print("Restoring from CSV...")

cinemas = pd.read_csv('cinemas.csv')


# scraping tools
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

##### Scrapers


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



# todo: add remaining scrapers
# todo: wrap scrapers in a try

# list all listings results
frames = [listings, listings01, listings02, listings03]
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

# save as CSV
listings.to_csv('listings.csv', index=False)
print("Results saved.")
