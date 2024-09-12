from typing import List

def create_section(title, bullets: List[List[str]]) -> str:
    """
    Create a section of the newsletter
    """
    links = "\n".join([f'<li><a href="{link}">{text}</a></li>' for text, link in bullets])
    section = f"""
        <section>
            <h2>{title}</h2>
            <ul>
                {links}
            </ul>
        </section>
    """
    return section