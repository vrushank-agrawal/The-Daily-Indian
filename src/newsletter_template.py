import os
import base64

from components import header, footer, styles, top_news
from typing import List, Dict

from components import sections


def newsletter_summary(news_summaries: List[str]) -> str:
    """ Create a summary for the newsletter header using the
        title summaries of the top news articles.
    """
    if not news_summaries:
        return ""

    return f"Today we are covering {news_summaries[0]}, {news_summaries[1]}, {news_summaries[2]}, and other top stories."


def newsletter_template(
    date: str,
    sections_news: List[Dict[str, List[List[str]]]],
    top_news_summaries: List[str] = []
) -> str:
    """ Create an html email message
    """

    image = "https://thedailyindian.vercel.app/images/logo.jpeg"
    header_summary_string = newsletter_summary(top_news_summaries)
    styles_string = styles.create_head()
    header_string = header.create_header(date, image, header_summary_string)
    topNews_string = top_news.create_body(sections_news["top_news"])
    sections_news.pop("top_news")
    section_string = sections.create_sections(sections_news)
    footer_string = footer.create_footer()

    # <<! <img src="cid:image1" alt="Indian Gospel" width="150" height="150"> >>

    html = f"""
        <!DOCTYPE html>
        <html lang="en">

        {styles_string}

        <body class="body-canvas">

        {header_string}

        {topNews_string}

        {section_string}

        {footer_string}

        </body>

        </html>
    """
    return html
