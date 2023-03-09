# Indie cinema scraper

Scraper to aggregate listings from independent cinemas in Toronto. Designed to feed a frontend webapp.

## status

Major items to work on:
- Get additional cinemas listed.
- Add  logging to report per-cinema results
- improve console messages so 1 line per listing, always, and progress is evident
- wrap components in trycatch to address error states:
  - no listings found
  - listing database update failure (consider not importing previously scraped data if it produces compare errors)

Cinemas completed so far:
- Cinesphere
- Tiff Bell Lightbox 
- cineplexes (template script done)
  - YD (7130)
  - Varsity (7199)
  - Yonge-eg (7400)
  - Beaches (7293)
  - Don Mills (7139)
  - Yorkdale (7406)
  - Empress walk (7298)
  - scotiabank (7402)
  - Fairview Mall (7115)
  - odeon eglington town center (7253)
  - Tiff Digital Cinema 
- The Revue
- The fox
 
Cinemas to do:
- Paradise
- Carleton
- Imagine Cinema Market Square
- Hot Docs
- Hot Docs at Home

Bugs:
- Timezone is not working correctly. Most import correctly as TZ-aware -5 Toronto but some save as -4. Unsure how this is possible or what creates this behaviour. 
- Subsequently, they are being converted into TZ-naive values when loaded into the database, relative to the database tz. This guarantees time errors. It is possible to load as tz-aware (maybe by changing the model datatypes?)