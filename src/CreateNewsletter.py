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
from components import newsletter
import pandas as pd
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import smtplib
import os
from dotenv import load_dotenv
load_dotenv()

class NewsLetterHandler:

    def __init__(self) -> None:
        pass

    def __fetch_analyzed_data(self) -> None:
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


    def create_newsletter(self) -> str:
        """ Create a newsletter from the sections data
        """

        self.__fetch_analyzed_data()
        self.__html = newsletter.newsletter_template(self.__date, self.__sections)
        print("Newsletter created")


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


if __name__ == "__main__":
    newsletter = NewsLetterHandler()
    newsletter.create_newsletter()
    newsletter.send_newsletter()