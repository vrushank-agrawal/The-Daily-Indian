import pandas as pd
from typing import List, Dict
from utils.read_write_IO import get_data, write_data

class FilterArticles:
    """ This class filters the articles based on sentiment  .

    :param __filtered_articles: The filtered articles.
    :rtype __filtered_articles: List[dict]
    """

    def __init__(self,
        articles: List[dict],
    ) -> None:
        self.__df = pd.DataFrame(articles)
        self.__filtered_articles = []
        # self.__pos_articles_removed = []


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


    def __remove_more_neutral_news(self) -> None:
        """ Removes rows with positive sentiment score less than neutral sentiment score.
        """

        # Elements where the first sentiment is neutral and higher than the second sentiment score
        first_neutral_news = self.__df[self.__df['sentiment'].apply(lambda x: x[0] == 'neutral')]
        first_news_to_remove = first_neutral_news[first_neutral_news['sentiment_score'].apply(lambda x:(x[0] > x[1]))]
        # self.__pos_articles_removed.extend(first_news_to_remove.to_dict('records'))

        # Elements where the second sentiment is neutral and higher than the first sentiment score
        second_neutral_news = self.__df[self.__df['sentiment'].apply(lambda x: x[1] == 'neutral')]
        second_news_to_remove = second_neutral_news[second_neutral_news['sentiment_score'].apply(lambda x: (x[1] > x[0]))]
        # self.__pos_articles_removed.extend(second_news_to_remove.to_dict('records'))

        self.__df = self.__df[~self.__df.index.isin(first_news_to_remove.index)]
        self.__df = self.__df[~self.__df.index.isin(second_news_to_remove.index)]


    def __remove_low_sentiment_news(self) -> None:
        """ Removes rows where the sentiment score is less than 0.6 for both sentiments.
        """

        less_positive_news = self.__df[self.__df['sentiment_score'].apply(lambda x: x[0] < 0.6 and x[1] < 0.6)]
        # self.__pos_articles_removed.extend(less_positive_news.to_dict('records'))
        self.__df = self.__df[~self.__df.index.isin(less_positive_news.index)]


    def post_sentiment_analysis_run(self) -> None:
        """ Sets the list of articles.
        """

        self.__remove_all_non_positive_news()
        self.__remove_BS_markets_news()
        self.__remove_all_politics_news()
        self.__remove_more_neutral_news()
        self.__remove_low_sentiment_news()

        self.__filtered_articles = self.__df.to_dict('records')
        write_data(self.__filtered_articles, 'filtered')
        # write_data(self.__pos_articles_removed, 'less_pos_news')


if __name__ == "__main__":
    from utils.constants import COLS_TO_FILTER, DISPLAY_CATEGORIES
    articles = get_data('sentiment')
    filtered = FilterArticles(articles, COLS_TO_FILTER, DISPLAY_CATEGORIES)
    filtered.post_sentiment_analysis_run()
