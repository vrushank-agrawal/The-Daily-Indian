from transformers import pipeline
from typing import List
from ReadWriteIO import get_data, write_data

# Load the sentiment analysis model
DEFAULT_MODEL = "ProsusAI/finbert"

class SentimentAnalyzer:
    """
    This class adds sentiment analysis to a list of articles.

    :param __articles: A list of articles.
    :param __model: The sentiment analysis model.
    """

    def __init__(self,
        articles: List[dict],
        model: str = DEFAULT_MODEL,
    ) -> None:
        self.__articles = articles
        self.__model = model


    def run_sentiment_analyzer(self) -> None:
        """
        Adds sentiment analysis to a list of articles.

        Modifies the articles in-place by adding 'sentiment' and 'sentiment_score' keys
        to each article dictionary.
        """

        # Load the sentiment analysis pipeline
        sentiment_pipeline = pipeline(
            "sentiment-analysis",
            model=self.__model,
            tokenizer=self.__model
        )

        # Iterate over the articles
        for article in self.__articles:

            # Analyze the sentiment of the article title
            title_input = article['title'] if len(article['title']) < 511 else article['title'][:511]
            title_result = sentiment_pipeline(title_input)

            # Analyze the sentiment of the article description
            description_input = article['description'] if len(article['description']) < 511 else article['description'][:511]
            description_result = sentiment_pipeline(description_input)

            article['sentiment'] = (title_result[0]['label'], description_result[0]['label'])
            article['sentiment_score'] = (title_result[0]['score'], description_result[0]['score'])

        # Print the number of articles analyzed
        print(f'Article analyzed: {len(self.__articles)}')

        write_data(self.__articles, 'sentiment')


if __name__ == "__main__":
    articles = get_data('cleaned')
    SentimentAnalyzer(articles).run_sentiment_analyzer()