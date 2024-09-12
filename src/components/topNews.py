from typing import List

def create_post(title, text) -> str:
    """
    Create a post for the body of the newsletter.

    :param title: The title of the post.
    :type title: str

    :param text: The text of the post.
    :type text: str
    """
    post = f"""
        <h3>{title}</h3>
        {text}
    """
    return post


def create_body(posts: List[List[str]]) -> str:
    """
    Create the body of the newsletter
    """
    posts = "\n".join([ "<hr>" + create_post(title, text) for title, text in posts])
    return f"""
    <div class="container">
        {posts}
    </div>
    """
