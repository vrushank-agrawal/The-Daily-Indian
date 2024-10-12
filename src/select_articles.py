import pandas as pd
from typing import List, Dict
from utils.read_write_IO import get_data, write_data

class SelectArticles:
    """ This class selects the top 3 articles from each category.

    :param __selected_articles: The selected articles for each category as a dict.
    """

    def __init__(self,
        articles: List[dict],
        cols_to_drop: List[str],
        categories_to_get: List[str],
    ) -> None:
        self.__df = pd.DataFrame(articles)
        self.__cols_to_drop = cols_to_drop
        self.__categories_to_get = categories_to_get
        self.__selected_articles = {}


    def __maximize_sentiment_score(self) -> None:
        """ Sets the sentiment score of the articles to the maximum of all scores.
        """
        self.__df['sentiment_score'] = self.__df['sentiment_score'].apply(lambda x: max(x))


    def __sort_by_sentiment_score(self) -> None:
        """ Sorts the articles by sentiment score in descending order.
        """
        self.__df = self.__df.sort_values(by='sentiment_score', ascending=False)


    def __select_top_three(self, category: str) -> None:
        """ Selects the top 3 articles from each category.

        :param category: The category to select the top 3 articles from.
        """

        cat_df = self.__df[self.__df['category'] == category]

        # TODO - Check if any of the top 3 articles are not India related
        self.__selected_articles[category] = cat_df.head(3)


    def __select_top_x(self, num: int, category: str = "top") -> None:
        """ Selects the top x articles from the specified category.

        :param category: The category to select the top x articles from. Defaults to "top".
        :param num: The number of articles to select.
        """

        cat_df = self.__df[self.__df['category'] == category]
        self.__selected_articles[category] = cat_df.head(num)


    def __drop_cols(self, cat: str) -> None:
        """ Drops the specified columns from the given category dataframe.

        :param cat: The category to drop the columns from.
        """
        self.__selected_articles[cat].drop(self.__cols_to_drop, axis=1, inplace=True)


    def __convert_df_to_dict(self, cat: str) -> None:
        """ Converts the dataframe to a dictionary.

        :param cat: The category to convert the dataframe to a dictionary.
        """
        self.__selected_articles[cat] = self.__selected_articles[cat].to_dict('records')


    def run(self) -> None:
        """ Selects the top 3 articles from each category.
        """

        self.__maximize_sentiment_score()
        self.__sort_by_sentiment_score()
        for cat in self.__categories_to_get:
            if cat == "top":
                self.__select_top_x(8, cat)
            else:
                self.__select_top_three(cat)
            self.__drop_cols(cat)
            self.__convert_df_to_dict(cat)

        write_data(self.__selected_articles, 'selected')


if __name__ == "__main__":
    from utils.constants import COLS_TO_DROP, CATEGORIES_TO_GET
    articles = get_data('sentence')
    selected = SelectArticles(articles, COLS_TO_DROP, CATEGORIES_TO_GET)
    selected.run()
