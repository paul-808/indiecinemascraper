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


########### Scraper 2: Tiff Bell Lightbox

url = cinemas["listingURL"][1]
print('attempting ' + url)

# Need javascript for this one, get webdriver and firefox spooled up:
browser = webdriver.Firefox()
browser.set_window_size(900, 900)
browser.set_window_position(0, 0)
browser.get(url)
page = Soup(browser.page_source, features="html.parser")
browser.quit()

# get films from upcoming
rawResults = page.find('div', {'class': re.compile('style__results_.*')})
rawFilmDays = rawResults.find_all('span', string=re.compile('.*(Sunday|Monday|Tuesday|Wednesday|Thursday|Friday|Saturday).*'))
nrawFilmDays = len(rawFilmDays)
# iterate through all DAYS
for d in range(nrawFilmDays):
    rawFilmDay = rawFilmDays[d].find_parent()
    rawFilmDate = rawFilmDay.find_all('h2')
    mMonth = re.search("(?i)January|February|March|April|May|June|July|August|September|October|November|December", rawFilmDate[0].text).group().strip()
    mDay = re.search(r"\d{1,2}", rawFilmDate[0].text).group().strip()

    # this day, if in this year, occurs on:
    mDateTest = datetime.strptime(str(datetime.now().year) + ' ' + mMonth + ' ' + mDay, '%Y %B %d')
    # is it more than 30 days in the past?
    delta = mDateTest - datetime.now()
    # if so, keep current year, if in past, increment by one
    if delta.days < -30:
        mYear = str(datetime.now().year + 1)
    else:
        mYear = str(datetime.now().year)

    # get films from upcoming
    rawFilms = rawFilmDay.find_all('div', {'class': re.compile("style__resultCard.*")})
    nrawFilms = len(rawFilms)

    # iterate through all FILMS
    for i in range(nrawFilms):
        mTitle = rawFilms[i].find('span').text
        print(mTitle)
        mURL = 'https://www.tiff.net/calendar' + rawFilms[i].select('a')[0].attrs['href']
        mPoster = rawFilms[i].find('div', {'class': re.compile("style__cardImg.*")})['style']
        mPoster = re.search(r'(?<=").*(?=(\?|"))', mPoster).group()

        # iterate through all TIMES
        mTimes = rawFilms[i].find_all('div', {'class': re.compile("style__screeningButton.*")})
        nmTimes = len(mTimes)

        for t in range(nmTimes):
            mHour = re.search(r"\d+(?=:)", mTimes[t].text).group()
            mMin = re.search(r"(?<=:)\d+", mTimes[t].text).group()
            mAMPM = re.search(r"(?i)(?<=\d:\d\d)(AM|PM)", mTimes[t].text).group().upper()
            mTime = datetime.strptime(mYear + ' ' + mMonth + ' ' + mDay + ' ' + mHour + ' ' + mMin + ' ' + mAMPM, '%Y %B %d %I %M %p')

            # append all to the list
            listing = []
            listing.append(pd.to_datetime("today"))
            listing.append(cinemas["name"][1])
            listing.append(mTitle)
            listing.append(mTime)
            listing.append(mURL)
            listing.append(mPoster)
            # append listing to listings dataframe
            listings.loc[len(listings)] = listing

listings.to_csv('listings.csv', index=False)



