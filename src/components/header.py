from datetime import datetime

def create_header():
    """
    Create the header of the newsletter
    """
    now = datetime.now()
    # write the date in Weekday, Day Month format
    date = now.strftime("%A, %d %B")

    header = f"""
        <header>
            <h1>The Indian Gospel</h1>

            <p><strong>Good Morning!. It's {date},</strong></p>

            <p><strong>First time reading?</strong> <a href="https://www.indiangospel.com/first-time-reading">Sign up here</a></p>

            <p>As always, <strong>We love feeback</strong>. Write to us at <a href="mailto:feedback@indiangospel.com">feedback@indiangospel.com</a></p>
        </header>
    """
    return header