def scrape_03_cineplex(cinemaID, locationID):
    from urllib import request
    from bs4 import BeautifulSoup
    import datetime
    import json
    import pandas as pd

    # initiate empty data frame for local listings
    listings_local = pd.DataFrame(columns=['timestamp', 'cinema', 'mTitle', 'mTime', 'mURL', 'mPosterURL'])

    # Set constants for the cinema using the listing master
    cinemas = pd.read_csv('cinemas.csv')
    mCinema = cinemas['name'][cinemaID]

    # probably unnecessary df to track URLS that return listings
    urls = pd.DataFrame(columns=['date', 'url'])

    # just hammer the next 30 days, because it's tricky to get the real list of available dates
    for i in range(30):
        trydate = datetime.datetime.now() + datetime.timedelta(days=i)
        url = "https://www.cineplex.com/api/v1/theatres/"+str(locationID)+"/availablemovies/showtimesoneposter?language=en-us&marketLanguageCodeFilter=false&showDate="+str(trydate.year)+"-"+'{:02d}'.format(trydate.month)+"-"+'{:02d}'.format(trydate.day)
        print('attempting ' + url)
        html = request.urlopen(url).read()
        soup = BeautifulSoup(html, 'html.parser')
        site_json = json.loads(soup.text)
        if len(site_json["data"]) > 0 :
            dateChecked = [trydate]
            dateChecked.append(url)
            urls.loc[len(urls)] = dateChecked

            for rawMovie in site_json["data"]:
                print(rawMovie["movie"]["name"])
                mTitle = rawMovie["movie"]["name"]
                mUrl = cinemas["listingURL"][cinemaID] # no unique movie URLs, default to cinema URL
                mPosterUrl = rawMovie["movie"]["largePosterImageUrl"] # medium and small variants available

                for rawShowtime in rawMovie["showtimeDetails"][0]["showtimes"]:
                    mTime = datetime.datetime.strptime(rawShowtime["showStartDateTimeUtc"], '%Y-%m-%dT%H:%M:%SZ')
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
        else:
            print("no showtimes on "+str(trydate))

    # return the results object
    return listings_local