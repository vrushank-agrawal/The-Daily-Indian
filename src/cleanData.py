import json
import pandas as pd
from datetime import datetime, timezone

TODAY_DATE = datetime.now(timezone.utc).strftime("%Y-%m-%d")

def clean_cols(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove certain columns of a DataFrame of articles.

    :param articles: A DataFrame of articles.
    :type articles: pd.DataFrame
    """
    # Drop unnecessary columns
    cols = ['ai_tag',
            'ai_region',
            'ai_org',
            'content',
            'image_url',
            'source_icon',
            'video_url',
            'country',
            'keywords',
            'language',
            'sentiment_stats',
            'source_id',
            'source_url',
            'source_priority',
            'creator',
            'article_id',
            'pubDateTZ',
            # 'duplicate'
            ]
    df = df.drop(columns=cols)
    return df


def clean_countries(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans the rows of a list of articles where the country is >1.

    :param articles: A list of articles.
    :type articles: list
    """
    # All rows with more than 1 country in the list should be removed
    df = df[df['country'].apply(len) == 1]

    return df


def clean_empty_descriptions(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans the rows of a list of articles where the description is empty.

    :param articles: A list of articles.
    :type articles: list
    """
    # All rows where json value is null should be removed
    df = df.dropna(subset=['description'])

    return df


def clean_sources(df: pd.DataFrame) -> pd.DataFrame:
    """
    Removes rows with certain sources from a list of articles.

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
                     'Deccan Chronicle',    # Hyderabad
                    )

    # All source_name integer values < '20000' should be kept
    df = df[df['source_priority'].isin(range(20000))]

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
    with open(f'data/newsdataio/articles/{TODAY_DATE}.json', 'r') as f:
        data = json.load(f)

    # Extract the list of articles from the JSON data.
    return data['articles']


def write_data(articles):
    """
    Writes a list of articles to the JSON file.

    Args:
        articles (list): The list of articles to write.
    """
    with open(f'data/newsdataio/cleaned/{TODAY_DATE}.json', 'w') as f:
        json.dump(articles, f, indent=4)


def set_the_hindu_keywords(df: pd.DataFrame) -> pd.DataFrame:
    """
    Sets the value of the category to that of keywords if the article is from the The Hindu.

    :param articles: A list of articles.
    :type articles: list
    """

    def return_category(keyword: str) -> str:
        """Maps The Hindu's keywords to a more general category."""
        category_map = {
            "markets": "business",
            "other sports": "sports",
            "movies": "entertainment",
            "india": "politics",
        }
        return category_map.get(keyword, keyword)

    for index, article in df.iterrows():
        if article['source_name'] == 'The Hindu':
            if article['category'] == ["top"]:
                df.at[index, 'category'] = [return_category(article['keywords'][0])]

    return df


def convert_category_to_string(df: pd.DataFrame) -> pd.DataFrame:
    """
    Converts the category column of a DataFrame to a string.

    :param articles: A DataFrame of articles.
    :type articles: pd.DataFrame
    """
    df['category'] = df['category'].apply(lambda x: x[0] if isinstance(x, list) else x)
    return df

def data_cleaner():
    """
    This function cleans the data in the JSON file containing a list of news articles.

    The function reads the JSON file, converts it into a pandas DataFrame, cleans the
    columns and rows of the DataFrame, and writes the cleaned DataFrame back to the
    JSON file.
    """
    articles = get_data()

    df = pd.DataFrame(articles)
    # df = clean_countries(df)
    # df = clean_sources(df)
    df = clean_empty_descriptions(df)
    df = set_the_hindu_keywords(df)
    df = convert_category_to_string(df)
    df = clean_cols(df)

    df.reset_index(drop=True, inplace=True)
    articles = df.to_dict('records')

    write_data(articles)


if __name__ == '__main__':
    data_cleaner()
