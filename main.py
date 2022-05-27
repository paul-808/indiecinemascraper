#####
## Indie Cinema Scraper
# v1.0
# Paul Jarvey
######

# load libraries
from urllib.request import urlopen, Request
from urllib.parse import urlparse
from bs4 import BeautifulSoup as soup
import pandas as pd

# setup data frame
## RUNONCE
listings = []

# datetime, Cinema index, Movie title, movie date, movie time, listing URL, movie poster url
# datetime, cinema, mTitle, mDate, mTime, mURL, mPosterUrl

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
temp = page.find_all('li', class_="filmBox")

#for each element in temp...
listing = []
listing.append(pd.to_datetime("today"))

listing.append("Cinesphere")

mtitle = temp[0].select('div a')[0].attrs['title']
listing.append(mtitle)

#works up to here

tempdate = temp[0].select('li.btn')

tempdate[0].getText


# list var order: datetime, cinema, mTitle, mDate, mTime, mURL, mPosterUrl

#follow this
# #https://www.dataquest.io/blog/web-scraping-python-using-beautiful-soup/