
def scrape_03_cinesphere(cinemaID):
    from urllib.request import urlopen, Request
    from urllib.parse import urlparse
    from bs4 import BeautifulSoup
    import datetime
    import json
    import re
    import pandas as pd
    # todo make sure this is actually working
    from scrapingTools import requestandparse


    # initiate empty data frame for local listings
    listings_local = pd.DataFrame(columns=['timestamp', 'cinema', 'mTitle', 'mTime', 'mURL', 'mPosterURL'])

    # Set constants for the cinema using the listing master
    cinemas = pd.read_csv('cinemas.csv')
    mCinema = cinemas['name'][cinemaID]
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
            mTitle = rawFilms[x].select('div a')[0].attrs['title']
            print(mTitle)

            # regex and construct time object
            mMonth = re.search("(?i)Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec", mTimes[i].text).group()
            mDay = re.search(r".\d(?=,)", mTimes[i].text).group().strip()
            mYear = re.search(r"2\d{3}", mTimes[i].text).group()
            mHour = re.search(r".\d(?=:\d\d)", mTimes[i].text).group().strip()
            mMin = re.search(r"(?<=\d:)\d\d", mTimes[i].text).group()
            mAMPM = re.search(r"(?i)(?<=\d:\d\d )(AM|PM)", mTimes[i].text).group()
            mTime = datetime.datetime.strptime(mYear + ' ' + mMonth + ' ' + mDay + ' ' + mHour + ' ' + mMin + ' ' + mAMPM,                                       '%Y %b %d %I %M %p')
            print(mTime)

            mURL = rawFilms[x].select('a')[0].attrs['href']
            mPosterUrl = rawFilms[x].select('img')[0].attrs['src']

            listing = []
            listing.append(pd.to_datetime("today"))
            listing.append(cinemas["name"][0])
            listing.append(mTitle)
            listing.append(mTime)
            listing.append(mURL)
            listing.append(mPosterUrl)

            # append listing to listings dataframe
            listings_local.loc[len(listings_local)] = listing


    # return the results object
    return listings_local