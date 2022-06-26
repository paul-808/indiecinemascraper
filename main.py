#####
# Indie Cinema Scraper
# v1.1
# May 27 2022
# Paul Jarvey
######

# temp stuff for building the new structure


# load libraries
from urllib.request import urlopen, Request
from urllib.parse import urlparse
from bs4 import BeautifulSoup as Soup
import pandas as pd
import re
import time
from datetime import datetime
from pathlib import Path

# gear up selenium w/ firefox
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
#NOTE: put geckodriver in vEnv path (type $PATH in terminal to get location)

from selenium.webdriver.firefox.options import Options
options = Options()
options.binary_location = "/usr/bin"
browser = webdriver.Firefox()


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


########### Scraper 1: Cinesphere

# run the request
url = cinemas["listingURL"][0]
print('attempting ' + url)
page, url = requestandparse(url)

# get films from upcoming
rawFilms = page.find_all('li', class_="filmBox")
nrawFilms = len(rawFilms)

for x in range(nrawFilms):

    # check if multiple times
    mTimes = rawFilms[x].find_all('li', class_='btn')
    nmTimes = len(mTimes)

    # per-film collection loop
    for i in range(nmTimes):
        # for each element in temp...
        listing = []
        listing.append(pd.to_datetime("today"))
        listing.append(cinemas["name"][0])
        mTitle = rawFilms[x].select('div a')[0].attrs['title']
        listing.append(mTitle)
        print(mTitle)

        # regex and construct time object
        mMonth = re.search("(?i)Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec", mTimes[i].text).group()
        mDay = re.search(r".\d(?=,)", mTimes[i].text).group().strip()
        mYear = re.search(r"2\d{3}", mTimes[i].text).group()
        mHour = re.search(r".\d(?=:\d\d)", mTimes[i].text).group().strip()
        mMin = re.search(r"(?<=\d:)\d\d", mTimes[i].text).group()
        mAMPM = re.search(r"(?i)(?<=\d:\d\d )(AM|PM)", mTimes[i].text).group()
        mTime = datetime.strptime(mYear + ' ' + mMonth + ' ' + mDay + ' ' + mHour + ' ' + mMin + ' ' + mAMPM, '%Y %b %d %I %M %p')
        listing.append(mTime)

        mURL = rawFilms[x].select('a')[0].attrs['href']
        listing.append(mURL)

        mPoster = rawFilms[x].select('img')[0].attrs['src']
        listing.append(mPoster)

        # append listing to listings dataframe
        listings.loc[len(listings)] = listing

listings.to_csv('listings.csv', index=False)




