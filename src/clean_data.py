import pandas as pd
from utils.read_write_IO import get_data, write_data
from typing import List

class DataCleaner:
    """
    This class cleans a list of articles.

    :param __df: A list of articles.
    :param __cols_to_clean: A list of columns to clean.
    """

    def __init__(self,
        articles: List[dict],
        cols_to_clean: List[str] = [],
    ) -> None:
        self.__df = pd.DataFrame(articles)
        self.__cols_to_clean = cols_to_clean

    def __set_the_hindu_keywords(self) -> None:
        """ Sets the value of the category to that of
            keywords if the article is from the The Hindu.
        """

        def return_category(keyword: str) -> str:
            """ Maps The Hindu's keywords to a more general category """

            category_map = {
                # "markets": "business",    # Markets have too much individual news
                "industry": "business",
                "movies": "entertainment",
                "india": "politics",
                "other sports": "sports",
                "cricket": "sports",
                "hockey": "sports",
                "football": "sports",
                "gadgets": "technology",
                "science": "technology",
                "world": "world",
            }
            return category_map.get(keyword, "top")

        for index, article in self.__df.iterrows():
            if article["source_name"] == 'The Hindu':
                if article['category'] == ["top"]:
                    self.__df.at[index, 'category'] = [return_category(article['keywords'][0])]


    def __convert_category_to_string(self) -> None:
        """ Converts the category column to string.
        """
        self.__df['category'] = self.__df['category'].apply(lambda x: x[0])


    def __remove_nulls(self) -> None:
        """ Removes all rows with no description or title.
        """

        self.__df = self.__df[self.__df['description'].notna()]
        self.__df = self.__df[self.__df['title'].notna()]


    def __remove_world_news(self) -> None:
        """ This is the India story so we don't need world news.
        """

        self.__df = self.__df[self.__df['category'] != 'world']

        # Remove all news which has the word '/world/' in the link
        self.__df = self.__df[~((self.__df['category'] == 'top') & (self.__df['link'].str.contains('/world/')))]

    def __drop_cols(self) -> None:
        """ Drops the specified columns from the dataframe.
        """
        self.__df.drop(self.__cols_to_clean, axis=1, inplace=True)


    def run(self) -> None:
        """ The entry function. Calls all other functions and
            cleans the data in the object df of news articles.
        """

        # TODO - Check if the india news in The Hindu is political

        self.__set_the_hindu_keywords()
        self.__convert_category_to_string()
        self.__remove_nulls()
        self.__remove_world_news()
        self.__drop_cols()
        self.__df.reset_index(drop=True, inplace=True)

        write_data(self.__df.to_dict('records'), 'cleaned')


if __name__ == '__main__':
    from utils.constants import COLS_TO_CLEAN
    articles = get_data('articles')
    DataCleaner(get_data('articles')['articles'], COLS_TO_CLEAN).run()
