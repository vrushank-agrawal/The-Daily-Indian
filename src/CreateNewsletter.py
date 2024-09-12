# Columns to clean from the raw API data
cols_to_clean = [
    'ai_tag',
    'ai_region',
    'ai_org',
    'article_id',
    'content',
    'country',
    'creator',
    'image_url',
    'keywords',
    'language',
    'pubDateTZ',
    'sentiment_stats',
    'source_icon',
    'source_id',
    'source_priority',
    'source_url',
    'video_url',
]

# Columns to remove from the dataframe after analysis
cols_to_delete = [
    'category',
    'duplicate',
    'pubDate',
    'sentiment',
    'sentiment_score',
    # 'source_name',
]

# Categories to get 3 articles each from
categories_to_get = [
    'business',
    'entertainment',
    'politics',
    'science',
    'sports',
]

from GetData import NewsArticles
from CleanData import DataCleaner
from SentimentAnalyzer import SentimentAnalyzer
from FilterArticles import FilterArticles
import pandas as pd

class NewsLetter:

    def __init__(self) -> None:
        pass


    def fetch_analyzed_data(self) -> None:
        """ Reads a JSON file containing a list of articles and returns the list of articles.
        """

        articles = NewsArticles()
        articles.fetch_all()

        cleaned_articles = DataCleaner(getattr(articles, '_NewsArticles__articles'), cols_to_clean)
        cleaned_articles.data_cleaner()

        df = getattr(cleaned_articles, '_DataCleaner__df')
        sentiment_analyzer = SentimentAnalyzer(df.to_dict('records'))
        sentiment_analyzer.run_sentiment_analyzer()

        analyzed_articles = getattr(sentiment_analyzer, '_SentimentAnalyzer__articles')

        filtered_articles = FilterArticles(analyzed_articles, cols_to_delete, categories_to_get)
        filtered_articles.get_articles()

        self.__sections = getattr(filtered_articles, '_FilterArticles__sections')

