import pandas as pd
from typing import List, Dict
from utils.read_write_IO import get_data, write_data

class FilterArticles2:
    """ This class filters the articles to remove similar articles.

    :param __articles: Top 3 articles from each category.
    """

    def __init__(self,
        articles: List[dict],
        similar_articles: List[List[int]],
    ) -> None:
        self.__articles = articles
        self.__similar_articles = similar_articles

    def __select_one_from_similar_articles(self) -> None:
        """ Selects the article with most positive sentiment score.
            Changes the category of the selected article to 'top_news'.
        """

        # TODO - Only select articles that are reported in more than 2 sources

        for i, similar_articles in enumerate(sorted(self.__similar_articles, key=len, reverse=True)):
            # find the article with the highest sentiment score
            highest_score, highest_article = 0, 0
            for article_num in similar_articles:
                sentiment_score_sum = sum(self.__articles[article_num]['sentiment_score'])
                if sentiment_score_sum > highest_score:
                    highest_score, highest_article = sentiment_score_sum, article_num

            # Mark the top 3 articles as top_news
            if i < 3:
                self.__articles[highest_article]['category'] = f'top_news'
                self.__articles[highest_article]['sentiment_score'] = [-i, -i]

            # Make the article mandatory to be picked by setting the sentiment score to 1
            else:
                self.__articles[highest_article]['sentiment_score'] = [1, 1]

            similar_articles.remove(highest_article)


    def __remove_other_similar_articles(self) -> None:
        """ Removes the non-selected similar articles.
        """

        # create a single list of all article numbers
        article_nums = set()
        for similar_articles in self.__similar_articles:
            article_nums = article_nums.union(similar_articles)

        # remove the non-selected articles in decreasing order
        for article_num in sorted(article_nums, reverse=True):
            self.__articles.pop(article_num)


    def post_sentence_similarity_run(self) -> None:
        """ Sets the list of articles.
        """

        self.__select_one_from_similar_articles()
        self.__remove_other_similar_articles()

        write_data(self.__articles, 'sentence')


if __name__ == "__main__":
    articles = get_data('sentiment')
    from sentence_similarity import SentenceSimilarity
    sentence_similarity = SentenceSimilarity(articles)
    similar_articles = getattr(sentence_similarity, '_SentenceSimilarity__similar_articles')
    filtered = FilterArticles2(articles, similar_articles)
    filtered.post_sentence_similarity_run()
