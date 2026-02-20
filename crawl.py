import argparse
from bs4 import BeautifulSoup
import requests
import time
import re

NASA_URL = "https://data.nasa.gov"
DATASETS_URL = "https://data.nasa.gov/dataset/"


def parse_args():
    parser = argparse.ArgumentParser(
        description="Scrape NASA by tag."
    )

    parser.add_argument(
        "--tag",
        type=str,
        required=True,
        help="Tag to filter datasets"
    )

    parser.add_argument(
        "--out",
        type=str,
        required=True,
        help="Output JSONL file path"
    )

    return parser.parse_args()


def get_soup(url):
    response = requests.get(url)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")


def collect_dataset_urls(tag):
    dataset_urls = set()

    search_url = f"{DATASETS_URL}/?tags={tag}"
    soup = get_soup(search_url)
    max_pages = 1 # int(soup.find_all(class_="page-link")[-2].text) TODO

    for page in range(1, max_pages+1):
        time.sleep(1)
        search_url = f"{DATASETS_URL}/?tags={tag}&page={page}"
        soup = get_soup(search_url)

        for a in soup.find_all(attrs={"aria-label": re.compile("Navigate to dataset:")}):
            dataset_urls.add(NASA_URL + a["href"])
    print(dataset_urls)



def main():
    args = parse_args()

    tag = args.tag
    output_file = args.out
    print(f"Scraping datasets with tag: {tag}")
    print(f"Writing results to: {output_file}")

    collect_dataset_urls(tag)


if __name__ == "__main__":
    main()