from typing import Dict, List

def combine_sections(sections: List[Dict[str, str]]) -> str:
    """ Combine all bullets in correct format
    """

    links = ""
    for section in sections:
        link = f"""
            <li class="m-top-10">&#8594; {section["title"]}.
                <a href="{section["link"]}"> More here</a>
            </li>
        """
        links += link

    return links


def create_section(title, bullets: List[Dict[str, str]]) -> str:
    """ Create a section of the newsletter
    """

    links = combine_sections(bullets)
    section = f"""
        <section class="section-text m-top-0">
            <hr class="m-top-0">
            <h2 class="section-title background-light-blue">{title.title()}</h2>
            <ul class="arrow">
                {links}
            </ul>
        </section>
    """
    return section


def create_sections(sections_news: List[Dict[str, List[List[str]]]]) -> str:
    """ Create all sections in correct format
    """

    sections_string = "".join([create_section(key, value) for key, value in sections_news.items()])

    return f"""
        <section class="section-text m-top-0">

            <h2 class="section-title background-light-green">In The Know</h2>

        </section>

        {sections_string}
    """