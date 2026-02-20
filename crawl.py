import argparse
from bs4 import BeautifulSoup
import requests
import time
import re
import json
import os
from tqdm import tqdm


NASA_URL = "https://data.nasa.gov"
DATASETS_URL = "https://data.nasa.gov/dataset"

session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept-Language": "en-US,en;q=0.9"
})


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
    response = session.get(url, timeout=15)
    response.raise_for_status()
    time.sleep(1.5)
    return BeautifulSoup(response.text, "html.parser")


def collect_dataset_urls(tag):
    dataset_urls = set()

    search_url = f"{DATASETS_URL}/?tags={tag}"
    soup = get_soup(search_url)
    max_pages = int(soup.find_all(class_="page-link")[-2].text)
    print("\nCollecting dataset urls...")

    for page in tqdm(range(1, max_pages+1)):
        search_url = f"{DATASETS_URL}/?tags={tag}&page={page}"
        soup = get_soup(search_url)

        for a in soup.find_all(attrs={"aria-label": re.compile("Navigate to dataset:")}):
            dataset_urls.add(NASA_URL + a["href"])

    return sorted(list(dataset_urls))


def collect_record(url, path):
    data = {
        "dataset_url":url, 
        "title": None,
        "description": None,
        "tags": [],
        "resource_links": [],
        "landing_page": None,
        "text_sources": [DATASETS_URL, url]
        }
    
    soup = get_soup(url)

    main_text = soup.find(
        class_="primary col-md-9 col-xs-12"
        ).find(
            "div",
            class_="module-content"
            )
    data["title"] = main_text.find("h1").text
    data["description"] = main_text.find(class_="notes embedded-content").find("p").text
    data["tags"].extend([tag["title"] for tag in main_text.find_all("a", class_="tag")])
    
    if main_text.find("p", class_="empty") != None:
        data["resource_links"].extend(
            [resource["href"] for resource in main_text.find_all("a", class_="heading")]
            )
    
    landing_page = main_text.find("th", string="landingPage")
    if landing_page != None:
        data["landing_page"] = landing_page.find_next_sibling("td", class_="dataset-details").text

    with open(path, 'a') as f:
        f.write(json.dumps(data) + "\n")
    


def main():
    args = parse_args()

    tag = args.tag
    output_file = args.out
    if os.path.exists(output_file):
        delete = input(f"File {output_file} already exists. Continue[y/n]? ")
        if 'n' in delete:
            quit()

    # create empty file from scratch
    with open(output_file, 'w'):
        pass

    print(f"Scraping datasets with tag: {tag}")
    print(f"Writing results to: {output_file}")

    dataset_urls = collect_dataset_urls(tag)
    print(f"Number of collected dataset urls: {len(dataset_urls)}")

    for dataset in tqdm(dataset_urls):
        collect_record(dataset, output_file)


if __name__ == "__main__":
    main()