from components import header, footer, styles, top_news
from typing import List, Dict

from components import sections

def newsletter_template(
    date: str,
    sections_news: List[Dict[str, List[List[str]]]]
) -> str:
    """ Create an html email message
    """

    styles_string = styles.create_head()
    header_string = header.create_header(date)
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
