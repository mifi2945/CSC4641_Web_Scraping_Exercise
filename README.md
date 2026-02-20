# How to Run
```
usage: crawl.py [-h] --tag TAG --out OUT

Scrape NASA by tag.

options:
  -h, --help  show this help message and exit
  --tag TAG   Tag to filter datasets
  --out OUT   Output JSONL file path
```

Note the OUT has to have the `.jsonl` extension. **If the file already exists, the program will prompt if you want to continue**:
- y: **will overwrite the existing file**
- n: will terminate the program without overwriting

# Assumptions
There were a few unclear instructions within the directions given on Canvas. Some of these are now assumptions:

1. The links under "Data and Resources" don't actually have to be visited/downloaded; they just need to be added to the list in the jsonl
2. The "landing_page" is just the landing page url in "Additional Info"
3. The "text_sources" are just all visited links where the scraper looked and stored data from


# Issues
A big big issue was that even during initial testing with getting a request just to the listing page, the requests would consistently time-out, making it near impossible to test or collect any data. This further elongated the collection process.

Needed to make a `session` for the requests so that the NASA website wasn't rate-limiting the requests.