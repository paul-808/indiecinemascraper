
def scrape_05_therevue(cinemaID):
    from urllib.request import urlopen, Request
    from urllib.parse import urlparse
    from bs4 import BeautifulSoup as Soup
    import datetime
    import json
    import re
    import pandas as pd
    #from main import requestandparse

    # initiate empty data frame for local listings
    listings_local = pd.DataFrame(columns=['timestamp', 'cinema', 'mTitle', 'mTime', 'mURL', 'mPosterURL'])

    # Set constants for the cinema using the listing master
    cinemas = pd.read_csv('cinemas.csv')
    mCinema = cinemas['name'][cinemaID]
    url = cinemas["listingURL"][cinemaID]
    print('attempting ' + url)
    page, url = requestandparse(url)

    # get films from upcoming
    rawFilmDays = page.find_all('div', class_="wpt_listing")
    nrawFilmDays = len(rawFilmDays)

    for x in range(nrawFilmDays):
        rawFilmDay = rawFilmDays[x].find('h3')
        mDay = re.search(r"\d{2}", rawFilmDay.text).group().strip()
        mMonth = re.search("(?i)January|February|March|April|May|June|July|August|September|October|November|December", rawFilmDay.text).group()

        rawFilms = rawFilmDays[x].find_all('div', class_="wp_theatre_event")

        for rawFilm in rawFilms:
            mHour = re.search(r"\d+(?=:\d\d)", rawFilm.select('div.wp_theatre_event_starttime')[0].text).group().strip()
            mMin = re.search(r"(?<=\d:)\d{2}", rawFilm.select('div.wp_theatre_event_starttime')[0].text).group().strip()
            mAMPM = re.search(r"(?i)(AM|PM)", rawFilm.select('div.wp_theatre_event_starttime')[0].text).group().strip()
            mTitle = re.search(r"[^-]*", rawFilm.select('div.wp_theatre_event_title a')[0].text).group().strip()

            print(mTitle + ' ' + mMonth + mDay)
            if mTitle == "Closed For Private Rental":
                continue

            mURL = rawFilm.select('div.wp_theatre_event_title a')[0].attrs['href']
            mPosterUrl = ""

            mYear = datetime.datetime.today().year
            mTime1 = datetime.datetime.strptime(str(mYear) + ' ' + str(mMonth) + ' ' + str(mDay) + ' ' + str(mHour) + ' ' + str(mMin) + ' ' + mAMPM,'%Y %B %d %I %M %p')
            mTime2 = datetime.datetime.strptime(str(mYear+1) + ' ' + str(mMonth) + ' ' + str(mDay) + ' ' + str(mHour) + ' ' + str(mMin) + ' ' + mAMPM,'%Y %B %d %I %M %p')

            if mTime1 < datetime.datetime.today():
                mTime = mTime1
            else:
                mTime = mTime2
            print(mTime)

            listing = []
            listing.append(pd.to_datetime("today"))
            listing.append(mCinema)
            listing.append(mTitle)
            listing.append(mTime)
            listing.append(mURL)
            listing.append(mPosterUrl)

            # append listing to listings dataframe
            listings_local.loc[len(listings_local)] = listing

    # return the results object
    print("The Revue complete, returning results....")
    return listings_local