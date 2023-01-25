
def scrape_04_cineplex(cinema_ID):
    from urllib import request
    from bs4 import BeautifulSoup
    import json
    import datetime
    import pandas as pd
    import numpy as np
    import pytz

    # initiate empty data frame for local listings
    listings_local = pd.DataFrame(columns=['timestamp', 'cinema', 'cinema_ID', 'mTitle', 'mTime', 'mURL', 'mPosterURL'])

    # Set constants for the cinema using the listing master
    cinemas = pd.read_csv('cinemas.csv')
    mCinema = cinemas['name'][cinema_ID]
    t_zone = cinemas['timezone'][cinema_ID]
    url = "https://tiff.net/filmlisttemplatejson"
    print('attempting ' + url)

    # load the listing
    html = request.urlopen(url).read()
    soup = BeautifulSoup(html, 'html.parser')
    site_json = json.loads(soup.text)

    for rawMovie in site_json["digitalItems"]:
        print(rawMovie["title"])
        mTitle = rawMovie["title"]
        mUrl = "https://tiff.net/events"+rawMovie["url"]
        if 'posterUrl' in rawMovie:
            mPosterUrl = "https:"+rawMovie["posterUrl"]
        elif 'img' in rawMovie:
            mPosterUrl = "https:"+rawMovie["img"]
        else:
            mPosterUrl = ""

        mTime = np.nan

        # append to listings list
        listing = []
        listing.append(datetime.datetime.now(pytz.timezone(t_zone)))
        listing.append(mCinema)
        listing.append(cinema_ID)
        listing.append(mTitle)
        listing.append(mTime)
        listing.append(mUrl)
        listing.append(mPosterUrl)

        # append listing to listings dataframe
        listings_local.loc[len(listings_local)] = listing

    # return the results object
    return listings_local