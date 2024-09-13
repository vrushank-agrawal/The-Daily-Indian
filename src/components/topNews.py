from typing import Dict ,List

def create_posts(articles: List[Dict[str, str]]) -> str:
    """ Create all post in correct format
    """
    
    html = ""
    for article in articles:
        title = article["title"]
        text = article["text"]
        html += f"""
            <h3>{title}</h3>
            {text}
        """
    return html


def create_body(posts: List[Dict[str, str]]) -> str:
    """ Create the top news section of the newsletter
    """
    posts = create_posts(posts)
    return f"""
    <div class="container">
        {posts}
    </div>
    """
