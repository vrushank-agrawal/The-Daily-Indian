import os
import requests
import json
from datetime import datetime, timedelta, timezone
from typing import Dict
from utils.exceptions import APIError
from utils.constants import START_TIME_DELAY, TIME_WINDOW, MAX_CALLS_PER_15_MIN, INCLUDE_DOMAINS
from dotenv import load_dotenv
load_dotenv()


class NewsArticles():
    """
    This class fetches articles from the NewsData.io API.

    :param __articles: The articles fetched from the API
    :rtype: dict

    :param __start_time: The start time from when the articles were fetched
    """

    def __init__(self, country: str = "in", lang: str = "en") -> None:
        self.__country = country
        self.__lang = lang
        self.__query_page = 0
        self.__start_time = datetime.now() - timedelta(minutes=START_TIME_DELAY)
        self.__articles = {"articles": [],}
        print("Start time: ", self.__start_time)
        print("End time: ", self.__start_time + TIME_WINDOW)

    def __define_url(self) -> str:
        """ Return a URL to query the NewsData.io API for articles. """

        url = (
            f'https://newsdata.io/api/1/latest?'
            f'apikey={self.__api_key}'
            f'&country={self.__country}'
            f'&language={self.__lang}'
            f'&domainurl={INCLUDE_DOMAINS}'
        )

        if self.__query_page:
            url += f'&page={str(self.__query_page)}'

        return url


    def __extend_page(self) -> None:
        """ Fetch articles from a single page from the NewsData.io API. """

        url = self.__define_url()

        try:
            response = requests.get(url)
        except Exception as e:
            raise APIError(str(e))

        data = json.loads(response.text)

        if 'status' in data and data['status'] == 'error':
            raise APIError(data["results"]["message"])

        self.__articles['articles'].extend(data['results']) if data['results'] else None
        self.__query_page = data['nextPage']


    def __fetch_block(self) -> bool:
        """
        Fetch all articles from the NewsData.io API in the defined Time Block
        in descending order of publication time.

        :return: True if all articles were fetched, False otherwise
        :rtype: bool
        """

        calls = 0

        while calls < MAX_CALLS_PER_15_MIN:
            calls += 1
            self.__extend_page()

            # Get the pub time of the last article fetched
            # Convert the time to a datetime object
            last_fetched_article_time = self.__articles['articles'][-1]['pubDate']
            last_fetched_article_time = datetime.strptime(last_fetched_article_time, "%Y-%m-%d %H:%M:%S")

            # If publication time > than current time, we've exhausted articles
            if last_fetched_article_time < self.__start_time:
                print(f'Fetched all articles for {TIME_WINDOW} minutes before {self.__start_time}')
                return True

        return False

    def run(self) -> None:
        """
        Fetches all articles from the NewsData.io API.

        Since the API paginates at 10 articles per page, we fetch articles in
        15 minute intervals. This is done until we reach our API limit of calls.
        """

        api1 = os.getenv("NEWSDATAIO_API_KEY")
        api2 = os.getenv("NEWSDATAIO_API_KEY_2")
        api3 = os.getenv("NEWSDATAIO_API_KEY_3")
        api4 = os.getenv("NEWSDATAIO_API_KEY_4")
        api5 = os.getenv("NEWSDATAIO_API_KEY_5")

        for i, api in enumerate([api1, api2, api3, api4, api5]):
            print(f'Using API key: {i+1}')
            self.__api_key = api
            all_fetched = self.__fetch_block()
            if all_fetched:
                break

        write_to_file(self.__articles)


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


if __name__ == '__main__':
    news = NewsArticles()
    news.run()
    write_to_file(getattr(news, '_NewsArticles__articles'))