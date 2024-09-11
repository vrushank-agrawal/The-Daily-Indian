import json
import pandas as pd

def clean_cols(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans the columns of a DataFrame of articles.

    :param articles: A DataFrame of articles.
    :type articles: pd.DataFrame
    """
    # Drop unnecessary columns
    cols = ['ai_tag', 'ai_region', 'ai_org',
            'content', 'image_url', 'source_icon',
            'video_url', 'country', 'language',
            'sentiment_stats', 'source_id', 'source_url',
            'creator', 'article_id', 'pubDateTZ',
            'duplicate']
    df = df.drop(columns=cols)
    return df


def clean_rows(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans the rows of a list of articles.

    :param articles: A list of articles.
    :type articles: list
    """
    # All rows with more than 1 country in the list should be removed
    df = df[df['country'].apply(len) == 1]

    return df


def clean_sources(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans the sources of a list of articles.

    :param articles: A list of articles.
    :type articles: list
    """
    local_sources = ('The Munsif Daily',    # Urdu Hyderabad
                     'Daily Excelsior',     # Kashmir
                     'Star of Mysore',      # Mysuru
                     'Tng News',            # Telangana
                     'Telangana Today',     # Telangana
                     'Odisha TV',           # Odisha
                     'In Ign',              # Games
                     'Gsm Arena',           # Mobile Phones
                     'Onmanorama',          # Kerala
                     'Mathrubhumi English', # Kerala
                    )

    # All source_name values < 20000 should be removed
    df = df[df['source_name'].str.len() < 20000]

    # All source_name values in local_sources should be removed
    df = df[~df['source_name'].isin(local_sources)]

    return df

def get_data():
    """
    Reads a JSON file containing a list of articles and returns the list of articles.

    Args:
        path (str): The path to the JSON file.

    Returns:
        list: The list of articles.
    """
    with open('data/newsdataio/articles.json', 'r') as f:
        # Load the JSON data from the file.
        # The 'data' variable is a dictionary with a single key 'articles',
        # the value of which is a list of article dictionaries.
        data = json.load(f)

    # Extract the list of articles from the JSON data.
    return data['articles']


def write_data(articles):
    """
    Writes a list of articles to the JSON file.

    Args:
        articles (list): The list of articles to write.
    """
    with open('data/newsdataio/articles.json', 'w') as f:
        json.dump(articles, f, indent=4)

def data_cleaner():
    """
    This function cleans the data in the JSON file containing a list of news articles.

    The function reads the JSON file, converts it into a pandas DataFrame, cleans the
    columns and rows of the DataFrame, and writes the cleaned DataFrame back to the
    JSON file.
    """
    articles = get_data()

    df = pd.DataFrame(articles)
    df = clean_cols(df)
    df = clean_rows(df)

    df.reset_index(drop=True, inplace=True)
    articles = df.to_dict('records')

    write_data(articles)


if __name__ == '__main__':
    data_cleaner()
