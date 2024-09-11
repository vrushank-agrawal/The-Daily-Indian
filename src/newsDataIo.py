import os
import requests
import json
from datetime import datetime, timedelta, timezone
import time
from typing import Tuple, Dict
from dotenv import load_dotenv
load_dotenv()

# API args
COUNTRY = "in"
LANG = "en"
API_KEY = os.getenv("NEWSDATAIO_API_KEY")
EXCLUDE_DOMAINS = "theweek.in,washingtontimes.com,firstpost.com"
INCLUDE_DOMAINS = "business-standard.com,thehindu.com,indianexpress.com,hindustantimes.com,economictimes.indiatimes.com"

# Maximum number of API calls to make in a 15 minute burst
MAX_CALLS = 25

# Number of API calls made in a day
API_LIMIT = 200

# Time Block to fetch articles from in minutes
TIME_BLOCK = 120

# Time difference between EST and news time in min
# I use EST because datetime is timezone aware
TIME_DIFF_MIN =  8 * 60 + 60 # hours * 60 + minutes


def define_url(page: int) -> str:
    """
    Return a URL to query the NewsData.io API for articles.

    :param page: The page of results to query. Pages start at 1.
    :type page: int

    :return: A URL to query the API.
    :rtype: str
    """
    url = ('https://newsdata.io/api/1/latest?'
           'apikey=' + API_KEY +
           '&country=' + COUNTRY +
           '&language=' + LANG +
           '&domainurl=' + INCLUDE_DOMAINS)

    if page:
        url = url + '&page=' + str(page)

    return url


def fetch_page(page: int) -> list:
    """
    Fetch articles from a single page from the NewsData.io API.

    :param page: The page of results to query.
    :type page: int

    :return: A list of articles.
    :rtype: list
    """
    url = define_url(page)
    response = requests.get(url)
    data = json.loads(response.text)
    articles = data['results']
    nextPage = data['nextPage']
    return articles, nextPage


def fetch_block() -> Tuple[Dict[str, list], int]:
    """
    Fetch all articles from the NewsData.io API in a Time Block.

    The API returns articles in descending order of publication time, so we
    fetch articles page by page until we reach articles that are older than
    the current time.

    :return: A json obj of articles.
    :rtype: dict

    :return: The number of API calls made.
    :rtype: int
    """
    start_time = datetime.now() - timedelta(minutes=TIME_DIFF_MIN)
    articles = {}
    articles['articles'] = []
    page = 0
    calls = 0

    while calls < MAX_CALLS:
        calls += 1
        articles_page, nextPage = fetch_page(page)
        articles['articles'].extend(articles_page)
        page = nextPage

        # Get the publication time of the last article we just fetched
        curr_time = articles['articles'][-1]['pubDate']
        # Convert the publication time to a datetime object
        curr_time = datetime.strptime(curr_time, "%Y-%m-%d %H:%M:%S")

        # If publication time > than current time, we've exhausted articles
        if curr_time < start_time:
            print(f'Fetched all articles in the {TIME_BLOCK} minutes after {start_time}')
            break

    return articles, calls


def write_to_file(articles: Dict[str, list]) -> None:
    """
    Writes a list of articles to a JSON file.

    :param articles: A list of articles.
    :type articles: list
    """
    date = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    with open(f'data/newsdataio/articles/{date}.json', 'w') as f:
        json.dump(articles, f, indent=4)

    print(f'Wrote {len(articles["articles"])} articles to articles.json')


def fetch_all():
    """
    Fetches all articles from the NewsData.io API.

    Since the API paginates at 10 articles per page, we fetch articles in
    15 minute intervals. This is done until we reach our API limit of calls.
    """
    total_calls = 0

    while total_calls < API_LIMIT:
        # Fetch articles in TIME_BLOCK intervals
        articles_page, calls = fetch_block()
        # Increment the total number of calls
        total_calls += calls

        # Write the articles to a JSON file
        write_to_file(articles_page)

        # Sleep for TIME_BLOCK minutes to avoid hitting the API limit
        time.sleep(TIME_BLOCK * 60)


if __name__ == '__main__':
    fetch_all()