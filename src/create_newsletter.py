import newsletter_template as newsletter_template
from get_data_from_API import NewsArticles
from clean_data import DataCleaner
from sentiment_analyzer import SentimentAnalyzer
from sentence_similarity import SentenceSimilarity
from filter_articles import FilterArticles
from filter_articles_2 import FilterArticles2
from select_articles import SelectArticles
from text_summarization import TextSummarization
from get_subscribers import GetSubscribers
from email_handler import EmailHandler

from utils.read_write_IO import get_data
from utils.constants import COLS_TO_CLEAN, COLS_TO_NOT_SELECT, DISPLAY_CATEGORIES
from utils.constants import MODEL_SENTIMENT_ANALYSIS, MODEL_SENTENCE_SIMILARITY, MODEL_TEXT_SUMMARIZATION

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

import os
from datetime import datetime, timezone
from dotenv import load_dotenv
load_dotenv()

TODAY_DATE = datetime.now(timezone.utc).strftime("%Y-%m-%d")

# TODO create a super class for environment variables
# and read write IO to be accessed by all subclasses

# TODO connect to an external db to regularly update data

# TODO create a class for different levels of Log Messages:
# Verbose: Info in development -> Not needed
# Trace: Info in development
# Info: Info in production
# Warning: Warning in production / development  ->  Send email?
# Error: Error in production / development  ->  Retry
# Critical: Critical in production / development

class NewsLetterHandler:
    """ This class creates a newsletter.

    :param __date: The date of the newsletter.
    :param __sections: The news sections of the newsletter.
    :param __html: The HTML of the newsletter.
    """

    def __init__(self) -> None:
        self.__date = datetime.now(timezone.utc).strftime("%A, %B %d, %Y")
        self.__sections = {}
        self.__html = ''
        self.__subject = f"The Daily Indian: {self.__date}"
        self.__environment = os.getenv("ENVIRONMENT")

    def __create_data(self) -> None:
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

        # self.__sections = get_data('selected')

        # TODO  Add another class for text summarization for the newsletter header.
        #       Modularize the code for text summarization through inheritance.

        # TODO  Add a custom model for text summarization instead of calling api

        # Title Text Summarizer
        summarizer = TextSummarization(self.__sections["top_news"], MODEL_TEXT_SUMMARIZATION)
        logged_in = summarizer.run()
        if logged_in:   # If logged in get the new subject
            self.__subject = getattr(summarizer, '_TextSummarization__subject')

        # TODO  Figure out the content format of top_news.
        #       Does the description need to be expanded?

        # TODO  Figure out the right categories to display.
        #       What really constitutes the India Story?



    def __modify_sections(self) -> None:
        """ If any section has no news then remove it.

        Rename top to other top articles
        """

        # Insert the sections in alphabetical order for the newsletter
        for title, articles in sorted(self.__sections.items(), key=lambda x: x[0]):
            self.__sections.pop(title)
            if articles == []:
                print("No articles for section: ", title)
            else:
                self.__sections.update({title: articles})

            print(title)

        exit()

        if "top" in self.__sections:
            top_articles = self.__sections["top"]
            self.__sections.pop("top")
            self.__sections.update({"Etcetera": top_articles})

    def run(self) -> None:
        """ Create a newsletter from the sections data
        """

        # self.__create_data()
        self.__sections = get_data('selected')
        self.__modify_sections()
        self.__html = newsletter_template.newsletter_template(self.__date, self.__sections)
        write_html(self.__html)
        print("Newsletter created")

        # self.__html = get_html()

        if self.__environment == 'production':
            print("Running in production")
            get_subscribers = GetSubscribers()
            get_subscribers.run()
            subscribers = getattr(get_subscribers, '_GetSubscribers__subscribers')
        else:
            print("Running in Development")
            subscribers = [
                # {"email": "Deepika.sangal@gmail.com", "name": "Subscriber"},
                {"email": "vrushank2001@gmail.com", "name": "Vrushank"}
            ]

        email_handler = EmailHandler(
            os.getenv("BREVO_API_KEY"),
            self.__subject,
            self.__html,
            subscribers
        )
        email_handler.send()
        print("Newsletter sent")


    # def send_newsletter(self) -> None:
    #     """ Send a newsletter email
    #     """

    #     print("Sending newsletter...")
    #     sender_email = os.getenv("SENDER_EMAIL")
    #     sender_password = os.getenv("SENDER_PASSWORD")
    #     receiver_email = os.getenv("RECEIVER_EMAIL")

    #     message = MIMEMultipart("alternative")
    #     message["Subject"] = "The Indian Gospel Daily Digest"
    #     message["From"] = sender_email
    #     message["To"] = receiver_email

    #     part = MIMEText(self.__html, "html")
    #     message.attach(part)

    #     # with open("src/utils/newsletter-logo.jpeg", "rb") as f:
    #     #     image = MIMEImage(f.read())
    #     # image.add_header("Content-ID", "<image1>")
    #     # message.attach(image)

    #     with smtplib.SMTP("smtp.gmail.com", 587) as server:
    #         server.ehlo()
    #         server.starttls()
    #         server.ehlo()
    #         server.login(sender_email, sender_password)
    #         server.sendmail(sender_email, receiver_email, message.as_string())

    #     print("Newsletter sent to {}".format(receiver_email))


def write_html(html: str) -> None:
    """
    Writes a list of articles to the JSON file.

    Args:
        articles (list): The list of articles to write.
    """
    with open(f'data/newsdataio/newsletter/{TODAY_DATE}.html', 'w') as f:
        f.write(html)

    print(f'Wrote Newsletter to newsletter.html')


def get_html() -> str:
    """
    Returns the HTML content of the newsletter.

    Returns:
        str: The HTML content of the newsletter.
    """
    with open(f'data/newsdataio/newsletter/{TODAY_DATE}.html', 'r') as f:
        html = f.read()

    return html


if __name__ == "__main__":
    newsletter = NewsLetterHandler()
    newsletter.run()
    # newsletter.send_newsletter()