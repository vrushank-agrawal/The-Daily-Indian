from transformers import pipeline
from typing import List
from ReadWriteIO import get_data, write_data

# Load the sentiment analysis model
MODEL = "cardiffnlp/twitter-roberta-base-sentiment-latest"

class SentimentAnalyzer:
    """
    This class adds sentiment analysis to a list of articles.

    :param __articles: A list of articles.
    :param __model: The sentiment analysis model.
    """

    def __init__(self,
        articles: List[dict],
        model: str = MODEL,
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

        # Initialize the counter for the number of articles analyzed
        articles_analyzed = 0

        # Iterate over the articles
        for article in self.__articles:
            # If the article has no description, skip it
            if not article['description']:
                article['sentiment'] = ""
                article['sentiment_score'] = ""
                continue

            # If the article description is too long, truncate it
            desc = article['description'][:511] if len(article['description']) > 511 else article['description']

            # Analyze the sentiment of the article
            articles_analyzed += 1
            result = sentiment_pipeline(desc)
            article['sentiment'] = result[0]['label']
            article['sentiment_score'] = result[0]['score']

        # Print the number of articles analyzed
        print(f'Article analyzed: {articles_analyzed}')

        write_data(self.__articles, 'sentiment')


if __name__ == "__main__":
    articles = get_data('cleaned')
    SentimentAnalyzer(articles).run_sentiment_analyzer()