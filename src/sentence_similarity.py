from sentence_transformers import SentenceTransformer
from typing import List
from utils.read_write_IO import get_data, write_data

# Load the default sentence similarity model
DEFAULT_MODEL = "sentence-transformers/all-mpnet-base-v2"

class SentenceSimilarity:
    """
    This class adds sentiment analysis to a list of articles.

    :param __articles: A list of articles.
    :param __model: The sentiment analysis model.
    :param __similarity_matrix: The similarity matrix.
    :param __similar_articles: The similar articles.
    """

    def __init__(self,
        articles: List[dict],
        model: str = DEFAULT_MODEL,
    ) -> None:
        self.__articles = articles
        self.__model = SentenceTransformer(model)
        self.__similarity_matrix = []
        self.__similar_articles: List[List[int]] = []


    def __create_similarity_matrix(self) -> None:
        """ Calculates the similarity matrix by running the model.
        """
        embeddings = self.__model.encode([article['title'] for article in self.__articles])
        self.__similarity_matrix = self.__model.similarity(embeddings, embeddings)


    def __print_similar_articles(self) -> None:
        """ Prints the similar articles.
        """

        already_printed = set()
        for i in range(len(self.__similarity_matrix)):
            if self.__articles[i]['title'] in already_printed:
                continue
            similar = []
            for j in range(len(self.__similarity_matrix)):
                if i != j and self.__similarity_matrix[i][j] > 0.5:
                    similar.append(self.__articles[j]['title'])
                    already_printed.add(self.__articles[j]['title'])

            if similar:
                print(self.__articles[i]["title"])
                for t in similar:
                    print(t)
                print('\n')


    def __find_similar_articles(self) -> None:
        """ Identifies similar articles and stores them in a list.
        """

        already_added = set()
        for i in range(len(self.__similarity_matrix)):
            if i in already_added:
                continue

            similar = []
            for j in range(len(self.__similarity_matrix)):
                if i != j and self.__similarity_matrix[i][j] > 0.5:
                    similar.append(j)
                    already_added.add(j)

            if similar:
                similar.append(i)
                already_added.add(i)
                self.__similar_articles.append(similar)


    def run(self) -> None:
        """ Runs sentence similarity analysis.
        """

        self.__create_similarity_matrix()
        # self.__print_similar_articles()

        self.__find_similar_articles()



if __name__ == "__main__":
    articles = get_data('filtered')
    SentenceSimilarity(articles).run()