import os
import requests
from typing import List
from dotenv import load_dotenv

load_dotenv()

class GetSubscribers:
    """ Fetches the list of subscribers from API.

    :param __subscribers: A list of subscribers. Where each
        subscriber is a dictionary with 'email' and 'name' keys.
    """

    def __init__(self) -> None:
        self.__subscribers = []


    # TODO Fetch subscribers directly from the db

    def __get_subscribers(self) -> List[dict]:
        url = "https://thedailyindian.vercel.app/api/subscribe"
        # url = "http://localhost:3000/api/subscribe"
        headers = {
            "apikey": os.getenv("INDIA_STORY_API_KEY"),
            "Authorization": f'Bearer {os.getenv("VERCEL_ACCESS_TOKEN")}',
            "Content-Type": "application/json",
        }
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            # Assuming the response is in JSON format
            subscribers = response.json()
            print(f"{len(subscribers)} subscribers fetched.")
        else:
            print(f"Failed to retrieve subscribers: {response.status_code}")

        self.__subscribers = subscribers


    def __convert_subscribers_to_email_list(self) -> None:
        """ Convert the list of subscribers to a list of emails.
        """
        email_list = [
                {
                    "email": subscriber['subscriber_email'],
                    "name": "Subscriber"
                }
                for subscriber in self.__subscribers
            ]
        self.__subscribers = email_list


    def run(self) -> None:
        """ Entry point to fetch subscribers.
        """
        self.__get_subscribers()
        self.__convert_subscribers_to_email_list()


if __name__ == "__main__":
    GetSubscribers().run()