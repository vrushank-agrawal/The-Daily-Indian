import json
import pandas as pd
from datetime import datetime, timezone
from typing import List

TODAY_DATE = datetime.now(timezone.utc).strftime("%Y-%m-%d")

class DataCleaner:
    """
    This class cleans a list of articles.

    :param __df: A list of articles.
    :param __cols_to_clean: A list of columns to clean.
    """

    def __init__(self,
        articles: List[dict],
        cols_to_clean: List[str] = [],
    ) -> None:
        self.__df = pd.DataFrame(articles)
        self.__cols_to_clean = cols_to_clean

    def __set_the_hindu_keywords(self) -> None:
        """
        Sets the value of the category to that of keywords if the article is from the The Hindu.
        """

        def return_category(keyword: str) -> str:
            """Maps The Hindu's keywords to a more general category."""
            category_map = {
                "markets": "business",
                "other sports": "sports",
                "movies": "entertainment",
                "india": "politics",
            }
            return category_map.get(keyword, keyword)

        for index, article in self.__df.iterrows():
            if article['source_name'] == 'The Hindu':
                if article['category'] == ["top"]:
                    self.__df.at[index, 'category'] = [return_category(article['keywords'][0])]


    def data_cleaner(self) -> None:
        """
        This function cleans the data in the object df of news articles.
        """

        # If article is from The Hindu, set the category to that of keywords
        self.__set_the_hindu_keywords()

        # Convert 'category' column to string
        self.__df['category'] = self.__df['category'].apply(lambda x: x[0])

        # Remove rows with no description
        self.__df = self.__df[self.__df['description'].notna()]

        # Drop columns to clean
        self.__df.drop(columns=self.__cols_to_clean, inplace=True)

        # Reset index
        self.__df.reset_index(drop=True, inplace=True)

        # Write the cleaned data to the JSON file
        write_data(self.__df.to_dict('records'))


def get_data() -> list:
    """
    Reads a JSON file containing a list of articles and returns the list of articles.

    Returns:
        list: The list of articles.
    """
    with open(f'data/newsdataio/articles/{TODAY_DATE}.json', 'r') as f:
        data = json.load(f)

    # Extract the list of articles from the JSON data.
    return data['articles']


def write_data(articles):
    """
    Writes a list of articles to the JSON file.

    Args:
        articles (list): The list of articles to write.
    """
    with open(f'data/newsdataio/cleaned/{TODAY_DATE}.json', 'w') as f:
        json.dump(articles, f, indent=4)


if __name__ == '__main__':
    from CreateNewsletter import cols_to_clean
    DataCleaner(get_data(), cols_to_clean).data_cleaner()
