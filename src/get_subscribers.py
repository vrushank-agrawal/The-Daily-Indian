import os
import requests
from typing import List
from dotenv import load_dotenv

load_dotenv()

class GetSubscribers:
    """ Fetches the list of subscribers from API.

    :param __subscribers: A list of subscribers.
    """

    def __init__(self) -> None:
        self.__subscribers = self.__get_subscribers()


    def __get_subscribers(self) -> List[dict]:
        url = "https://theindiastory.vercel.app/api/subscribe"
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
            print(subscribers)
        else:
            print(f"Failed to retrieve subscribers: {response.status_code}")

        return subscribers


if __name__ == "__main__":
    GetSubscribers()