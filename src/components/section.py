from typing import Dict, List

def combine_sections(sections: List[Dict[str, str]]) -> str:
    """ Combine all bullets in correct format
    """

    links = ""
    for section in sections:
        link = f"""
            <li>{section["title"]}.
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
        <section class="section">
            <h2 class="section-title">{title}</h2>
            <ul class="arrow">
                {links}
            </ul>
        </section>
    """
    return section