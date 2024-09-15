from components import header, footer, section, styles, top_news
from typing import List, Dict

def transform_section_to_single_dict(sections: List[Dict[str, List[Dict[str, str]]]]) -> Dict[str, List[List[Dict[str, str]]]]:
    """ Combine all sub dicts into a single dict
    """

    # Each entry of the list is a dict and each dict has ony a single key
    # Combine all these single key and value pairs from each dict into a single dict

    dic_ = {}

    for section in sections:
        for key, value in section.items():
            dic_[key] = value

    return dic_


def newsletter_template(
    date: str,
    sections_news: List[Dict[str, List[List[str]]]]
) -> str:
    """
    Create an html email message looking newsletter
    """

    sections_news = transform_section_to_single_dict(sections_news)
    styles_string = styles.create_head()
    header_string = header.create_header(date)
    topNews_string = top_news.create_body(sections_news["top_articles"])
    sections_news.pop("top_articles")
    section_string = "".join([section.create_section(key, value) for key, value in sections_news.items()])
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
