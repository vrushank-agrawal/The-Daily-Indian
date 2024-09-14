import pandas as pd
from typing import List, Dict
from ReadWriteIO import get_data, write_data

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


    def filter_articles(self) -> None:
        """ Sets the list of articles.
        """
        self.__sections = self.__get_top_three_articles()
        self.__sections.extend(self.__get_all_categories())

        write_data(self.__sections, 'filtered')


if __name__ == "__main__":
    from CreateNewsletter import cols_to_delete
    articles = get_data('sentiment')
    filtered = FilterArticles(articles, cols_to_delete)
    filtered.filter_articles()
