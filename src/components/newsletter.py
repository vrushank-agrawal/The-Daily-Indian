import header, footer, section, styles, topNews
from typing import List, Dict

def init_newsletter(
    date: str,
    top_news: List[List[str]],
    sections_news: Dict[str, List[List[str]]]
) -> str:
    """
    Create an html email message looking newsletter
    """

    styles_string = styles.create_head()
    header_string = header.create_header(date) + "\n<hr>"
    topNews_string = topNews.create_body(top_news) + "\n<hr>"
    section_string = "\n<hr>\n".join([section.create_section(key, value) for key, value in sections_news.items()]) + "\n<hr>"
    footer_string = footer.create_footer()

    # <<! <img src="cid:image1" alt="Indian Gospel" width="150" height="150"> >>

    html = f"""
        <!DOCTYPE html>
        <html lang="en">

        {styles_string}

        <body>

        {header_string}

        {topNews_string}

        {section_string}

        {footer_string}

        </body>

        </html>
    """
    return html

init_newsletter()