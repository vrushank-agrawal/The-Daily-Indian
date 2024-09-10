from transformers import pipeline
import json


MODEL = "cardiffnlp/twitter-roberta-base-sentiment-latest"

def get_data_from_file(path: str) -> list:
    with open(path, 'r') as f:
        data = json.load(f)

    return data['articles']


def append_sentiment_to_articles(articles: list) -> list:
    sentiment_pipeline = pipeline("sentiment-analysis", model = MODEL, tokenizer = MODEL)
    articles_analyzed = 0


    for article in articles:
        if not article['description'] or len(article['description']) == 0 or len(article['description']) > 511:
            article['sentiment'] = None
            article['sentiment_score'] = None
            continue

        articles_analyzed += 1
        result = sentiment_pipeline(article['description'])
        article['sentiment'] = result[0]['label']
        article['sentiment_score'] = result[0]['score']

    print(f'Article analyzed: {articles_analyzed}')
    return articles


def run_sentiment_analyzer():
    articles = get_data_from_file('data/newsdataio/articles.json')
    articles = append_sentiment_to_articles(articles)

    with open('data/newsdataio/sentiment-analysis-output.json', 'w') as f:
        json.dump(articles, f, indent=4)


if __name__ == "__main__":
    run_sentiment_analyzer()