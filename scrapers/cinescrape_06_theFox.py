
def scrape_06_thefox(cinema_ID):
    import datetime
    import re
    import pandas as pd
    import scrapers.scrapingTools


    # initiate empty data frame for local listings
    listings_local = pd.DataFrame(columns=['timestamp', 'cinema', 'cinema_ID', 'mTitle', 'mTime', 'mURL', 'mPosterURL'])

    # Set constants for the cinema using the listing master
    cinemas = pd.read_csv('cinemas.csv')
    mCinema = cinemas['name'][cinema_ID]
    url = cinemas["listingURL"][cinema_ID]
    print('attempting ' + url)
    page, url = scrapers.scrapingTools.requestandparse(url)

    # get films from upcoming
    rawFilms = page.find_all('article', class_="elementor-post")


    for rawFilm in rawFilms:
        mURL = rawFilm.select('a.elementor-post__thumbnail__link')[0].attrs['href']
        mPosterUrl = rawFilm.select('a.elementor-post__thumbnail__link div img')[0].attrs['src']
        mTitle = re.search(r"[^\-–]*", rawFilm.select('div.elementor-post__text h3')[0].text.strip()).group()
        mPage, mURL = scrapers.scrapingTools.requestandparse(mURL)

        showtimes = mPage.find_all('div', class_="elementor-shortcode")
        nShowtimes = len(showtimes[0].select("h5"))

        for x in range(nShowtimes):
            rawFilmDay = showtimes[0].select("h5")[x]
            mMonth = re.search("(?i)January|February|March|April|May|June|July|August|September|October|November|December", rawFilmDay.text).group()
            mDay = re.search(r"\d+", rawFilmDay.text).group().strip()
            rawFilmTime = showtimes[0].select("span")[x]
            mHour = re.search(r"\d+(?=:\d\d)", rawFilmTime.text).group().strip()
            mMin = re.search(r"(?<=\d:)\d{2}", rawFilmTime.text).group().strip()
            mAMPM = re.search(r"(?i)(AM|PM)", rawFilmTime.text).group().strip()

            mYear = datetime.datetime.today().year
            mTime1 = datetime.datetime.strptime(str(mYear) + ' ' + str(mMonth) + ' ' + str(mDay) + ' ' + str(mHour) + ' ' + str(mMin) + ' ' + mAMPM, '%Y %B %d %I %M %p')
            mTime2 = datetime.datetime.strptime(str(mYear + 1) + ' ' + str(mMonth) + ' ' + str(mDay) + ' ' + str(mHour) + ' ' + str(mMin) + ' ' + mAMPM, '%Y %B %d %I %M %p')

            if mTime1 > datetime.datetime.today():
                mTime = mTime1
            else:
                mTime = mTime2

            print(mTitle, ' ', mTime)

            listing = []
            listing.append(pd.to_datetime("today"))
            listing.append(mCinema)
            listing.append(cinema_ID)
            listing.append(mTitle)
            listing.append(mTime)
            listing.append(mURL)
            listing.append(mPosterUrl)

            # append listing to listings dataframe
            listings_local.loc[len(listings_local)] = listing

    # return the results object
    print("The Fox complete, returning results....")
    return listings_local
