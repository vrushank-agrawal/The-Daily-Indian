import json
from transformers import pipeline
from datetime import datetime, timezone
from typing import List

# Get today's date for filename
TODAY_DATE = datetime.now(timezone.utc).strftime("%Y-%m-%d")

# Load the sentiment analysis model
MODEL = "cardiffnlp/twitter-roberta-base-sentiment-latest"

class SentimentAnalyzer:

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


    def get_articles(self) -> List[dict]:
        """ Returns the list of articles.
        """
        return self.__articles


def get_data() -> list:
    """
    Reads a JSON file containing a list of articles and returns the list of articles.

    Returns:
        list: The list of articles.
    """
    with open(f'data/newsdataio/cleaned/{TODAY_DATE}.json', 'r') as f:
        data = json.load(f)

    # Extract the list of articles from the JSON data.
    return data


def write_data(articles):
    """
    Writes a list of articles to the JSON file.

    Args:
        articles (list): The list of articles to write.
    """
    with open(f'data/newsdataio/sentiment/{TODAY_DATE}.json', 'w') as f:
        json.dump(articles, f, indent=4)

    print(f'Wrote {len(articles)} articles to cleaned.json')


if __name__ == "__main__":
    articles = get_data()
    SentimentAnalyzer(articles).run_sentiment_analyzer()
    write_data(articles)