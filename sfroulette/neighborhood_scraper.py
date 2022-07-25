#! /usr/bin/env python
import argparse
import logging
import requests
from urllib.parse import urlparse


LOGGER = logging.getLogger(__file__)

WIKIPEDIA_API_URL = "https://en.wikipedia.org/w/api.php"
DEFAULT_NEIGHBORHOOD_URL = \
    "https://en.wikipedia.org/wiki/List_of_neighborhoods_in_San_Francisco"
USELESS_SECTIONS = (
    "See also", "References", "External links", "Specific neighborhoods"
)


def get_sections(page_title):
    response = requests.get(WIKIPEDIA_API_URL, params={
        "action": "parse",
        "page": page_title,
        "prop": "sections",
        "format": "json"
    })
    if response.status_code == 200:
        # the if statement is actually useless, as the api returns 200 even for
        # blatant errors ಠ_ಠ
        results = response.json()["parse"]
        return (item["line"] for item in results["sections"])


def is_this_section_a_neighborhood(section_name):
    return section_name not in USELESS_SECTIONS


def extract_title_from_url(url):
    parsed = urlparse(url)
    if parsed.path.startswith("/wiki/"):
        return parsed.path[len("/wiki/"):]


def get_neighborhoods_from_url(url):
    neighborhood_page_title = extract_title_from_url(url)
    LOGGER.info(f"Page title: {neighborhood_page_title}")
    all_sections = get_sections(neighborhood_page_title)
    return list(filter(is_this_section_a_neighborhood, all_sections))


if __name__ == "__main__":
    logging.basicConfig(format="%(message)s")

    parser = argparse.ArgumentParser()
    parser.add_argument("--neighborhood_url", default=DEFAULT_NEIGHBORHOOD_URL)
    parser.add_argument("-l", "--log_level", default="WARNING")
    args = parser.parse_args()

    LOGGER.setLevel(args.log_level)

    LOGGER.info(f"Using url: {args.neighborhood_url}")
    LOGGER.info(f"Using log level: {args.log_level}")

    neighborhoods = get_neighborhoods_from_url(args.neighborhood_url)

    LOGGER.info("Printing all neighborhoods:")
    for name in neighborhoods:
        print(name)
