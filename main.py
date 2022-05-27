#####
## Indie Cinema Scraper
# v1.1
# May 27 2022
# Paul Jarvey
######

# load libraries
import csv
from urllib.request import urlopen, Request
from urllib.parse import urlparse
from bs4 import BeautifulSoup as soup
import pandas as pd
import re
from datetime import datetime
from pathlib import Path

# Load data or init if none exists

if not Path('listings.csv').is_file():
    listings = pd.DataFrame(columns=['timestamp','cinema','mTitle','mTime','mURL','mPosterURL'])
    print("Historical data not found, initiating new...")
else:
    listings = pd.read_csv('listings.csv')
    print("Restoring from CSV...")

# set target
url = "https://ontarioplace.com/en/cinesphere/"

# format URLS
def checkURL(requested_url):
    if not urlparse(requested_url).scheme:
        requested_url = "https://" + requested_url
    return requested_url

#Set agent and request dat
def requestAndParse(requested_url):
    requested_url = checkURL(requested_url)
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
        request_obj = Request(url = requested_url, headers = headers)
        opened_url = urlopen(request_obj)
        page_html = opened_url.read()
        opened_url.close()
        page_soup = soup(page_html, "html.parser")
        return page_soup, requested_url

    except Exception as e:
        print(e)

# run the request
page, url = requestAndParse(url)

# get films from upcoming
rawFilms = page.find_all('li', class_="filmBox")
nrawFilms = len(rawFilms)

for x in range(nrawFilms):

    #check if multiple times
    mTimes = rawFilms[x].find_all('li', class_='btn')
    nmTimes = len(mTimes)

    # per-film collection loop
    for i in range(nmTimes):
        #for each element in temp...
        listing = []
        listing.append(pd.to_datetime("today"))
        listing.append("Cinesphere")
        mTitle = rawFilms[x].select('div a')[0].attrs['title']
        listing.append(mTitle)
        print(mTitle)

        # regex and construct time object
        mMonth = re.search("(?i)Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec", mTimes[i].text).group()
        mDay = re.search(".\d(?=,)", mTimes[i].text).group().strip()
        mYear = re.search("2\d{3}", mTimes[i].text).group()
        mHour = re.search(".\d(?=:\d\d)", mTimes[i].text).group().strip()
        mMin = re.search("(?<=\d:)\d\d", mTimes[i].text).group()
        mAMPM = re.search("(?i)(?<=\d:\d\d )(AM|PM)", mTimes[i].text).group()
        mTime = datetime.strptime(mYear + ' ' + mMonth + ' ' + mDay + ' ' + mHour + ' ' + mMin + ' ' + mAMPM, '%Y %b %d %I %M %p')
        listing.append(mTime)

        mURL = rawFilms[x].select('a')[0].attrs['href']
        listing.append(mURL)

        mPoster = rawFilms[x].select('img')[0].attrs['src']
        listing.append(mPoster)

        #append listing to listings dataframe
        listings.loc[len(listings)] = listing

listings.to_csv('listings.csv', index=False)

