import json
from typing import Dict
from datetime import datetime, timezone, timedelta
# Get today's date for filename in EST timezone.
TODAY_DATE = datetime.now(timezone(timedelta(hours=5))).strftime("%Y-%m-%d")


def get_data(sub_folder: str, main_folder: str = 'data/newsdataio', date: str = TODAY_DATE) -> Dict[str, list]:
    """
    Reads a JSON file containing a list of articles and returns the list of articles.

    Returns:
        list: The list of articles.
    """
    with open(f'{main_folder}/{sub_folder}/{date}.json', 'r') as f:
        data = json.load(f)

    # Extract the list of articles from the JSON data.
    return data


def write_data(articles: list, sub_folder: str, main_folder: str = 'data/newsdataio', date: str = TODAY_DATE) -> None:
    """
    Writes a list of articles to the JSON file.

    Args:
        articles (list): The list of articles to write.
    """
    with open(f'{main_folder}/{sub_folder}/{date}.json', 'w') as f:
        json.dump(articles, f, indent=4)

    print(f'Wrote {len(articles)} articles to {sub_folder}')
