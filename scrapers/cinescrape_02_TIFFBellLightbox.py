
def scrape_02_cineplex(cinema_ID):
    from urllib import request
    from bs4 import BeautifulSoup
    import datetime
    import json
    import pandas as pd
    import pytz

    # initiate empty data frame for local listings
    listings_local = pd.DataFrame(columns=['timestamp', 'cinema', 'cinema_ID', 'mTitle', 'mTime', 'mURL', 'mPosterURL'])

    # Set constants for the cinema using the listing master
    
    cinemas = pd.read_csv('cinemas.csv')
    t_zone = cinemas['timezone'][cinema_ID]
    mCinema = cinemas['name'][cinema_ID]
    url = "https://tiff.net/filmlisttemplatejson"
    print('attempting ' + url)

    # load the listing
    html = request.urlopen(url).read()
    soup = BeautifulSoup(html, 'html.parser')
    site_json = json.loads(soup.text)

    for rawMovie in site_json["items"]:
        print(rawMovie["title"])
        mTitle = rawMovie["title"]
        mUrl = "https://tiff.net/events"+rawMovie["url"]
        if 'posterUrl' in rawMovie:
            print("has poster")
            mPosterUrl = "https:"+rawMovie["posterUrl"]
        elif 'img' in rawMovie:
            print("has img")
            mPosterUrl = "https:"+rawMovie["img"]
        else:
            print("no image")
            mPosterUrl = ""

        for rawShowtime in rawMovie["scheduleItems"]:
            mTime = datetime.datetime.strptime(rawShowtime["startTime"], '%Y-%m-%d %H:%M:%S')
            mTime =  pytz.timezone(t_zone).localize(mTime)
            if datetime.datetime.now(pytz.timezone(t_zone)) > mTime:
                print("skipping - date in past")
                continue

            print(mTime)

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