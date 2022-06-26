
def scrape_01Cineplex(cinemaID):
    from urllib import request
    from bs4 import BeautifulSoup
    import datetime
    import json
    import pandas as pd
    # todo make sure this is actually working, not used for this cinema
    from scrapers import scrapingTools

    # initiate empty data frame for local listings
    listings_local = pd.DataFrame(columns=['timestamp', 'cinema', 'mTitle', 'mTime', 'mURL', 'mPosterURL'])

    # Set constants for the cinema using the listing master
    cinemas = pd.read_csv('cinemas.csv')
    mCinema = cinemas['name'][cinemaID]
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
        mPosterUrl = "https:"+rawMovie["posterUrl"]

        for rawShowtime in rawMovie["scheduleItems"]:
            mTime = datetime.datetime.strptime(rawShowtime["startTime"], '%Y-%m-%d %H:%M:%S')

            if pd.to_datetime("today") > mTime:
                print("skipping - date in past")
                continue

            print(mTime)

            # append to listings list
            listing = []
            listing.append(pd.to_datetime("today"))
            listing.append(mCinema)
            listing.append(mTitle)
            listing.append(mTime)
            listing.append(mUrl)
            listing.append(mPosterUrl)

            # append listing to listings dataframe
            listings_local.loc[len(listings_local)] = listing

    # return the results object
    return listings_local