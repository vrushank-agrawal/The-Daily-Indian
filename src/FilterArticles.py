import pandas as pd
from typing import List, Dict
from datetime import datetime, timezone
import json

TODAY_DATE = datetime.now(timezone.utc).strftime("%Y-%m-%d")

class FilterArticles:
    """ This class filters and selects the articles to be sent in the newsletter.

    :param __top_articles: The top 3 articles.
    :param __sections: Top 3 articles from each category.
    """

    def __init__(self,
        articles: List[dict],
        cols_to_drop: List[str],
        categories_to_get: List[str] = ['business', 'politics', 'entertainment', 'sports', 'world']
    ) -> None:
        self.__articles = articles
        self.__df = pd.DataFrame(articles)
        self.__cols_to_drop = cols_to_drop
        self.__categories_to_get = categories_to_get
        self.__sections = []


    def __drop_cols(self, df: pd.DataFrame) -> pd.DataFrame:
        """ Drops the specified columns from the dataframe.
        """
        df.drop(self.__cols_to_drop, axis=1, inplace=True)


    def __get_three_articles(self, category: str) -> Dict[str, List[dict]]:
        """ Returns the list of articles.
        """
        top_three = self.__df[self.__df['category'] == category].head(3)
        self.__drop_cols(top_three)
        as_list = top_three.to_dict('records')
        return { f'{category}' : as_list }


    def __get_all_categories(self) -> List[dict]:
        """ Gets the top 3 articles from each category.
        """
        return [self.__get_three_articles(cat) for cat in self.__categories_to_get]


    def __get_top_three_articles(self) -> List[Dict[str, List[dict]]]:
        """ Sets the latest three articles and removes them from the list.
        """
        top_articles = self.__articles[:3]
        self.__articles = self.__articles[3:]
        top_articles = pd.DataFrame(top_articles)
        self.__drop_cols(top_articles)
        top_articles = top_articles.to_dict('records')
        return [ { "top_articles" : top_articles } ]


    def get_articles(self) -> None:
        """ Sets the list of articles.
        """
        self.__sections = self.__get_top_three_articles()
        self.__sections.extend(self.__get_all_categories())


def get_data() -> list:
    """
    Reads a JSON file containing a list of articles and returns the list of articles.

    Returns:
        list: The list of articles.
    """
    with open(f'data/newsdataio/sentiment/{TODAY_DATE}.json', 'r') as f:
        data = json.load(f)

    # Extract the list of articles from the JSON data.
    return data


def write_data(sections):
    """
    Writes a list of articles to the JSON file.

    Args:
        articles (list): The list of articles to write.
    """
    with open(f'data/newsdataio/filtered/{TODAY_DATE}.json', 'w') as f:
        json.dump(sections, f, indent=4)

    print(f'Wrote articles to filtered.json')


if __name__ == "__main__":
    from CreateNewsletter import cols_to_delete
    articles = get_data()
    filtered = FilterArticles(articles, cols_to_delete)
    filtered.get_articles()
    write_data(
        getattr(filtered, '_FilterArticles__sections')
    )