import pandas as pd
from typing import List, Dict
from utils.read_write_IO import get_data, write_data

class FilterArticles:
    """ This class filters and selects the articles to be sent in the newsletter.

    :param __top_articles: The top 3 articles.
    :param __sections: Top 3 articles from each category.
    """

    def __init__(self,
        articles: List[dict],
        cols_to_drop: List[str],
        categories_to_get: List[str],
    ) -> None:
        self.__articles = articles
        self.__df = pd.DataFrame(articles)
        self.__cols_to_drop = cols_to_drop
        self.__categories_to_get = categories_to_get
        self.__sections = []


    def __remove_all_non_positive_news(self) -> None:
        """
        Removes all news articles who do not have a positive sentiment or have a negative sentiment
        """

        # Remove all non-positive news
        self.__df = self.__df[self.__df['sentiment'].apply(lambda x: x[0] == 'positive' or x[1] == 'positive')]

        # Remove all negative news
        to_remove = self.__df[self.__df['sentiment'].apply(lambda x: x[0] == 'negative' or x[1] == 'negative')]
        self.__df = self.__df[~self.__df.index.isin(to_remove.index)]


    def __remove_BS_markets_news(self) -> None:
        """ Remove all markets news from Business Standard.
        """

        rows_to_remove = self.__df[
            (self.__df['source_name'] == 'Business Standard')
            & (self.__df['link'].str.startswith('https://www.business-standard.com/markets/'))
        ]
        self.__df = self.__df[~self.__df.index.isin(rows_to_remove.index)]


    def __remove_all_politics_news(self) -> None:
        """ Remove all politics news from the category.
        """

        self.__df = self.__df[self.__df['category'] != 'politics']


    def __remove_all_less_positive_news(self) -> None:
        """ Removes rows with positive sentiment score less than neutral sentiment score.
        """

        # Elements where the first sentiment is neutral and higher than the second sentiment score
        first_neutral_news = self.__df[self.__df['sentiment'].apply(lambda x: x[0] == 'neutral')]
        first_news_to_remove = first_neutral_news[first_neutral_news['sentiment_score'].apply(lambda x: x[0] > x[1])]

        # Elements where the second sentiment is neutral and higher than the first sentiment score
        second_neutral_news = self.__df[self.__df['sentiment'].apply(lambda x: x[1] == 'neutral')]
        second_news_to_remove = second_neutral_news[second_neutral_news['sentiment_score'].apply(lambda x: x[1] > x[0])]

        self.__df = self.__df[~self.__df.index.isin(first_news_to_remove.index)]
        self.__df = self.__df[~self.__df.index.isin(second_news_to_remove.index)]


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


    def run(self) -> None:
        """ Sets the list of articles.
        """

        self.__remove_all_non_positive_news()
        self.__remove_BS_markets_news()
        self.__remove_all_politics_news()
        self.__remove_all_less_positive_news()

        self.__sections = self.__df.to_dict('records')

        # self.__sections = self.__get_top_three_articles()
        # self.__sections.extend(self.__get_all_categories())

        write_data(self.__sections, 'filtered')


if __name__ == "__main__":
    from utils.constants import COLS_TO_FILTER, DISPLAY_CATEGORIES
    articles = get_data('sentiment')
    filtered = FilterArticles(articles, COLS_TO_FILTER, DISPLAY_CATEGORIES)
    filtered.run()
