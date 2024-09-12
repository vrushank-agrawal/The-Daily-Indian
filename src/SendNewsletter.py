from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import smtplib
import os
from dotenv import load_dotenv
load_dotenv()

import src.getData as getData, src.CleanData as CleanData, src.SentimentAnalyzer as SentimentAnalyzer

def fetch_articles() -> list:
    """

    """

    articles = getData.get_data_from_file()
    articles = CleanData.clean_articles(articles)
    articles = SentimentAnalyzer.append_sentiment_to_articles(articles)
    return articles

def create_newsletter() -> str:
    """

    """



def send_newsletter():
    """
    Send an html email message looking newsletter
    """
    print("Sending newsletter...")
    sender_email = os.getenv("SENDER_EMAIL")
    sender_password = os.getenv("SENDER_PASSWORD")
    receiver_email = os.getenv("RECEIVER_EMAIL")

    message = MIMEMultipart("alternative")
    message["Subject"] = "The Indian Gospel Daily Digest"
    message["From"] = sender_email
    message["To"] = receiver_email

    html = create_newsletter()

    part = MIMEText(html, "html")

    message.attach(part)

    with open("src/utils/newsletter-logo.jpeg", "rb") as f:
        image = MIMEImage(f.read())

    image.add_header("Content-ID", "<image1>")

    message.attach(image)
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, message.as_string())

    print("Newsletter sent to {}".format(receiver_email))


if __name__ == "__main__":
    send_newsletter()