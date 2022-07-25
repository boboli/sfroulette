import random

from neighborhood_scraper import \
    get_neighborhoods_from_url, \
    DEFAULT_NEIGHBORHOOD_URL


if __name__ == "__main__":
    neighborhoods = get_neighborhoods_from_url(DEFAULT_NEIGHBORHOOD_URL)

    print(random.choice(neighborhoods))
