from transformers import pipeline
import json
from datetime import datetime, timezone

# Get today's date for filename
TODAY_DATE = datetime.now(timezone.utc).strftime("%Y-%m-%d")

# Load the sentiment analysis model
MODEL = "cardiffnlp/twitter-roberta-base-sentiment-latest"

def get_data_from_file() -> list:
    """
    Reads a JSON file containing a list of articles and returns the list of articles.

    Returns:
        list: The list of articles.
    """
    with open(f'data/newsdataio/cleaned/{TODAY_DATE}.json', 'r') as f:
        data = json.load(f)

    # Extract the list of articles from the JSON data.
    return data


def append_sentiment_to_articles(articles: list) -> list:
    """
    Adds sentiment analysis to a list of articles.

    Modifies the articles in-place by adding 'sentiment' and 'sentiment_score' keys
    to each article dictionary.

    Args:
        articles (list): List of article dictionaries

    Returns:
        list: The modified list of article dictionaries
    """
    # Load the sentiment analysis pipeline
    sentiment_pipeline = pipeline("sentiment-analysis", model = MODEL, tokenizer = MODEL)

    # Initialize the counter for the number of articles analyzed
    articles_analyzed = 0

    # Iterate over the articles
    for article in articles:
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
    return articles


def run_sentiment_analyzer():
    """
    Runs the sentiment analysis on the articles and save the results to a file.

    The sentiment analysis is run on the articles in the file
    'data/newsdataio/articles.json'. The results are saved to the file
    'data/newsdataio/sentiment-analysis-output.json'.
    """
    # Load the articles from the file
    articles = get_data_from_file()

    # Add the sentiment analysis to the articles
    articles = append_sentiment_to_articles(articles)

    # Save the results to a file
    with open(f'data/newsdataio/sentiment/{TODAY_DATE}.json', 'w') as f:
        json.dump(articles, f, indent=4)


if __name__ == "__main__":
    run_sentiment_analyzer()