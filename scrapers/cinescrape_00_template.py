# template

def scrape_00(cinema_ID, cinemas):
    from urllib.request import urlopen, Request
    from urllib.parse import urlparse
    from bs4 import BeautifulSoup
    import datetime
    import json
    import re
    import pandas as pd
    from main import requestandparse

    listings_local = pd.DataFrame(columns=['timestamp', 'cinema', 'mTitle', 'mTime', 'mURL', 'mPosterURL'])
    listing = []

    url = cinemas["listingURL"][cinema_ID]
    print('attempting ' + url)
    page, url = requestandparse(url)

    # scraper goes here

    # build the listing
    listing.append(pd.to_datetime("today"))
    listing.append(cinemas["name"][0])
    listing.append(mTitle)
    listing.append(mTime)
    listing.append(mURL)
    listing.append(mPoster)

    # append to listings list
    listings_local.loc[len(listings_local)] = listing

    # return the results object
    return listings_local