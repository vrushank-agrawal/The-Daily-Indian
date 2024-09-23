from typing import Dict ,List

def create_posts(articles: List[Dict[str, str]]) -> str:
    """ Create all post in correct format
    """

    html = ""
    for article in articles:
        title = article["title"]
        text = article["description"]
        html += f"""
            <hr>
            <h3>{title}</h3>
            {text}
        """
    return html


def create_body(posts: List[Dict[str, str]]) -> str:
    """ Create the top news section of the newsletter
    """
    posts = create_posts(posts)
    return f"""
    <div class="container section-text m-bottom-10">
        <h2 class="section-title background-light-green">Most Popular</h2>
        {posts}
    </div>
    """
