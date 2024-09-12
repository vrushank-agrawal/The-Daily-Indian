def create_header(date: str) -> str:
    """
    Create the header of the newsletter
    """

    header = f"""
        <header>
            <h1>The Indian Gospel</h1>

            <p><strong>Good Morning!. It's {date},</strong></p>

            <p><strong>First time reading?</strong> <a href="https://www.indiangospel.com/first-time-reading">Sign up here</a></p>

            <p>As always, <strong>We love feeback</strong>. Write to us at <a href="mailto:feedback@indiangospel.com">feedback@indiangospel.com</a></p>
        </header>
    """
    return header