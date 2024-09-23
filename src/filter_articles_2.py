from typing import List
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


    def __combine_overlapping_categories(self) -> None:
        """
        Several articles may be present in different categories because they
        are similar to articles that are not highly similar to each other.

        This function combines the overlapping articles in the same category.
        """

        for i in range(len(self.__similar_articles)):
            for j in range(i+1, len(self.__similar_articles)):
                i_articles = set(self.__similar_articles[i])
                j_articles = set(self.__similar_articles[j])

                if not j_articles:
                    continue

                if i_articles.intersection(j_articles):
                    self.__similar_articles[i] += self.__similar_articles[j]
                    self.__similar_articles[j] = []
                    print("Combined {} and {}".format(i, j))

        self.__similar_articles = [x for x in self.__similar_articles if x]


    def __select_top_from_similar_articles(self, similar_articles: List[int]) -> int:
        """ Selects one article from the list of similar articles.
        """

        multiples = {
            "neutral": 1,
            "positive": 1.5,
            "negative": 0.5
        }

        highest_score, highest_article = 0, 0
        for article_num in similar_articles:
            sentiment_score_sum = sum([multiples[x] * self.__articles[article_num]['sentiment_score'][i] for i, x in enumerate(self.__articles[article_num]['sentiment'])])
            if sentiment_score_sum > highest_score:
                highest_score, highest_article = sentiment_score_sum, article_num

        return highest_article


    def __mark_top_articles(self, is_top_news: bool, article_num: int, score: int) -> None:
        """ Marks the top article for similar articles.

        :param index: The index of the article in the list of similar articles.
        :param article_num: The article number.
        :param score: The sentiment score of the article.
        """
        if is_top_news:   # Mark the top 3 articles as top_news
            print("Marked {} as top_news".format(article_num))
            self.__articles[article_num]['category'] = 'top_news'

        self.__articles[article_num]['sentiment_score'] = [score, score]


    def __find_articles_to_remove(self) -> None:
        """ Marks the articles with most positive sentiment score.
            Changes the category of the selected article to 'top_news'.
        """

        articles_to_remove = set()

        for i, similar_articles in enumerate(sorted(self.__similar_articles, key=len, reverse=True)):
            highest_article = self.__select_top_from_similar_articles(similar_articles)

            if i < 3:    # Mark the top 3 articles as top_news
                self.__mark_top_articles(True, highest_article, -i)
            elif len(similar_articles) > 2: # Imp if reported by more than 2 sources
                self.__mark_top_articles(False, highest_article, len(similar_articles))

            articles_to_remove.update(similar_articles)
            articles_to_remove.remove(highest_article)

        return articles_to_remove


    def __remove_other_similar_articles(self, articles_to_remove: set) -> None:
        """ Removes the non-selected similar articles.

        :param articles_to_remove: The articles to remove.
        """

        # remove the non-selected articles in descending order
        for num in sorted(articles_to_remove, reverse=True):
            self.__articles.pop(num)


    def post_sentence_similarity_run(self) -> None:
        """ Sets the list of articles.
        """

        self.__combine_overlapping_categories()
        articles_to_remove = self.__find_articles_to_remove()
        self.__remove_other_similar_articles(articles_to_remove)

        write_data(self.__articles, 'sentence')


if __name__ == "__main__":
    articles = get_data('filtered', date='2024-09-22')
    from sentence_similarity import SentenceSimilarity
    sentence_similarity = SentenceSimilarity(articles)
    sentence_similarity.run()
    similar_articles = getattr(sentence_similarity, '_SentenceSimilarity__similar_articles')
    filtered = FilterArticles2(articles, similar_articles)
    filtered.post_sentence_similarity_run()
