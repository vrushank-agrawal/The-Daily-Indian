import json
from datetime import datetime, timezone
# Get today's date for filename
TODAY_DATE = datetime.now(timezone.utc).strftime("%Y-%m-%d")


def get_data(sub_folder: str, main_folder: str = 'data/newsdataio') -> list:
    """
    Reads a JSON file containing a list of articles and returns the list of articles.

    Returns:
        list: The list of articles.
    """
    with open(f'{main_folder}/{sub_folder}/{TODAY_DATE}.json', 'r') as f:
        data = json.load(f)

    # Extract the list of articles from the JSON data.
    return data


def write_data(articles: list, sub_folder: str, main_folder: str = 'data/newsdataio') -> None:
    """
    Writes a list of articles to the JSON file.

    Args:
        articles (list): The list of articles to write.
    """
    with open(f'{main_folder}/{sub_folder}/{TODAY_DATE}.json', 'w') as f:
        json.dump(articles, f, indent=4)

    print(f'Wrote {len(articles)} articles to {sub_folder}')
