import newsletter_template as newsletter_template
from get_data_from_API import NewsArticles
from clean_data import DataCleaner
from sentiment_analyzer import SentimentAnalyzer
from sentence_similarity import SentenceSimilarity
from filter_articles import FilterArticles
from filter_articles_2 import FilterArticles2
from select_articles import SelectArticles

from utils.read_write_IO import get_data
from utils.constants import COLS_TO_CLEAN, COLS_TO_NOT_SELECT, DISPLAY_CATEGORIES
from utils.constants import MODEL_SENTIMENT_ANALYSIS, MODEL_SENTENCE_SIMILARITY

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

import os
from datetime import datetime, timezone
from dotenv import load_dotenv
load_dotenv()

TODAY_DATE = datetime.now(timezone.utc).strftime("%Y-%m-%d")

class NewsLetterHandler:
    """ This class creates a newsletter.

    :param __date: The date of the newsletter.
    :param __sections: The news sections of the newsletter.
    :param __html: The HTML of the newsletter.
    """

    def __init__(self) -> None:
        self.__date = datetime.now(timezone.utc).strftime("%A, %B %d, %Y")
        self.__sections = []
        self.__html = ''

    def __fetch_analyzed_data(self) -> None:
        """ Reads a JSON file containing a list of articles and returns the list of articles.
        """

        # Get data from API
        articles = NewsArticles()
        articles.run()
        articles = getattr(articles, '_NewsArticles__articles')['articles']

        # Clean data
        cleaner = DataCleaner(articles, COLS_TO_CLEAN)
        cleaner.run()
        df = getattr(cleaner, '_DataCleaner__df')

        # Analyze sentiment
        sentiment_analyzer = SentimentAnalyzer(df.to_dict('records'), MODEL_SENTIMENT_ANALYSIS)
        sentiment_analyzer.run()
        analyzed_articles = getattr(sentiment_analyzer, '_SentimentAnalyzer__articles')

        # Filter articles
        filterer = FilterArticles(analyzed_articles)
        filterer.post_sentiment_analysis_run()
        filtered_articles = getattr(filterer, '_FilterArticles__filtered_articles')

        # filtered_articles = get_data('filtered')

        # Sentence similarity
        sentence_similarity = SentenceSimilarity(filtered_articles, MODEL_SENTENCE_SIMILARITY)
        sentence_similarity.run()
        similar_articles = getattr(sentence_similarity, '_SentenceSimilarity__similar_articles')

        # Filter articles after sentence similarity
        filterer2 = FilterArticles2(filtered_articles, similar_articles)
        filterer2.post_sentence_similarity_run()
        filtered_articles_2 = getattr(filterer2, '_FilterArticles2__articles')

        # Select articles
        selector = SelectArticles(filtered_articles_2, COLS_TO_NOT_SELECT, DISPLAY_CATEGORIES)
        selector.run()
        self.__sections = getattr(selector, '_SelectArticles__selected_articles')


    def create_newsletter(self) -> str:
        """ Create a newsletter from the sections data
        """

        self.__fetch_analyzed_data()
        # self.__sections = get_data('filtered')

        # generate_news_summary

        # self.__html = newsletter_template.newsletter_template(self.__date, self.__sections)
        # print("Newsletter created")

        # write_html(self.__html)


    def send_newsletter(self) -> None:
        """ Send a newsletter email
        """

        print("Sending newsletter...")
        sender_email = os.getenv("SENDER_EMAIL")
        sender_password = os.getenv("SENDER_PASSWORD")
        receiver_email = os.getenv("RECEIVER_EMAIL")

        message = MIMEMultipart("alternative")
        message["Subject"] = "The Indian Gospel Daily Digest"
        message["From"] = sender_email
        message["To"] = receiver_email

        part = MIMEText(self.__html, "html")
        message.attach(part)

        # with open("src/utils/newsletter-logo.jpeg", "rb") as f:
        #     image = MIMEImage(f.read())
        # image.add_header("Content-ID", "<image1>")
        # message.attach(image)

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, message.as_string())

        print("Newsletter sent to {}".format(receiver_email))


def write_html(html: str) -> None:
    """
    Writes a list of articles to the JSON file.

    Args:
        articles (list): The list of articles to write.
    """
    with open(f'data/newsdataio/newsletter/{TODAY_DATE}.html', 'w') as f:
        f.write(html)

    print(f'Wrote Newsletter to newsletter.html')


if __name__ == "__main__":
    newsletter = NewsLetterHandler()
    newsletter.create_newsletter()
    # newsletter.send_newsletter()