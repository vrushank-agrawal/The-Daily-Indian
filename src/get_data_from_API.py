import os
import requests
import json
from datetime import datetime, timedelta, timezone
from time import sleep
from typing import Dict, List
from utils.exceptions import APIError
from utils.constants import (
    TIME_WINDOW,
    TIME_WINDOW_MONDAY,
    START_TIME_DELAY,
    START_TIME_DELAY_MONDAY,
    MAX_CALLS_PER_15_MIN,
    INCLUDE_DOMAINS,
    DAILY_API_LIMIT
)
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
        self.__articles = {"articles": [],}

        # Modify the start time based on the day of the week
        self.__day = datetime.now(timezone.utc).strftime("%A")
        self.__time_delay = START_TIME_DELAY if self.__day != "Monday" else START_TIME_DELAY_MONDAY
        self.__time_window = TIME_WINDOW if self.__day != "Monday" else TIME_WINDOW_MONDAY
        self.__start_time = datetime.now() - timedelta(minutes=self.__time_delay)

        print("Day: ", self.__day)
        print("Start time: ", self.__start_time)
        print("End time: ", self.__start_time + timedelta(minutes=int(self.__time_window)))


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

            # Get the pub time of the last article fetched & convert to a datetime object
            last_fetched_article_time = self.__articles['articles'][-1]['pubDate']
            last_fetched_article_time = datetime.strptime(last_fetched_article_time, "%Y-%m-%d %H:%M:%S")

            # If publication time > than current time, we've exhausted articles
            if last_fetched_article_time < self.__start_time:
                print(f'Fetched all articles for {self.__time_window} minutes after {self.__start_time}')
                return True

        return False


    def __fetched_all_articles(self, apis: List[str]) -> bool:
        """ Fetches all articles from the NewsData.io API for past 1 day.

        :param apis: A list of API keys
        :type apis: list
        :return: True if all articles were fetched, False otherwise
        :rtype: bool
        """

        for i, api in enumerate(apis):
            print(f'Using API key: {i+1}')
            self.__api_key = api
            all_fetched = self.__fetch_block()
            if all_fetched:
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
        apis = [api1, api2, api3, api4, api5]

        # Fetch all articles in 16 minute intervals until API limit reached
        calls = 0
        while (not (self.__fetched_all_articles(apis)) and (DAILY_API_LIMIT - calls < MAX_CALLS_PER_15_MIN)):
            calls += MAX_CALLS_PER_15_MIN   # 30 calls per 15 minutes
            print(f'Last article fetched at: {self.__articles["articles"][-1]["pubDate"]}')
            print(f'API calls remaining: {DAILY_API_LIMIT - calls}')
            print('Sleeping for 16 minutes...')
            sleep(60*16)                    # 16 minutes

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