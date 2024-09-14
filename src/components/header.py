def create_header(date: str, news_summary: str = "") -> str:
    """
    Create the header of the newsletter
    """

    header = f"""
        <header class="header section-text">
            <h1 class="title">The Indian Gospel</h1>

            <hr>

            <p class="m-top-30"><strong>Good Morning! It's {date}.</strong> {news_summary}</p>

            <p><strong>First time reading?</strong> Join thousands of like-minded change makers who get this newsletter daily. &nbsp;<a class="button" href="https://www.indiangospel.com/first-time-reading">Sign up here</a></p>

            <p><strong>We love feedback from our readers!</strong> If we missed something, you have any suggestions, or you just want to say hi please write to us at &nbsp;<a class="button" href="mailto:feedback@indiangospel.com">feedback@indiangospel.com</a></p>
        </header>
    """
    return header