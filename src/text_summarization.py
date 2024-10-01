import torch
from transformers import pipeline
from transformers.pipelines.base import Pipeline
from huggingface_hub import HfApi, login
from typing import List, Dict
from utils.read_write_IO import get_data

import json
import os
from dotenv import load_dotenv
load_dotenv()

DEFAULT_MODEL = "google/gemma-2-2b-it"
MODEL_TEMPERATURE = 0.3
MAX_TOKENS = 4096
TOP_P = 0.3

class TextSummarization:
    """ Class for summarizing the top news articles.

    Parameters
    ----------
    articles : List[Dict[str, str]]
        The top news articles to be summarized.
    model : str
        The summarization model to be used.

    Attributes
    ----------
    __subject : str
        The summaries of the top news articles as a subject line.
    """

    def __init__(self, articles: List[Dict[str, str]], model: str = DEFAULT_MODEL) -> None:
        self.__top_news_articles = articles
        self.__model = model
        self.__subject: str = ""


    def __hugging_face_login(self) -> int:
        """ Tries to log into Hugging Face Hub.

        Returns
        -------
        int
            1 if logged in successfully, 0 otherwise.
        """

        api = HfApi()

        try:
            user_info = api.whoami()
            print(f'Logged in as: {user_info["name"]}')

        except:
            print('Not logged in. Logging in...')
            login(os.getenv('HUGGINGFACE_READ_API_KEY'))

            try:
                user_info = api.whoami()
                print(f'Logged in as: {user_info["name"]}')

            except:
                print('Failed to login. Exiting...')
                return 0

        return 1


    def __extract_titles(self) -> List[str]:
        """ Extracts the titles of the top news articles.
        """
        titles = [article['title'] for article in self.__top_news_articles]
        return titles


    def __prompt_engineered_input(self, titles: List[str]) -> str:
        """ Generate the input prompt for the summarization model.
        """

        return f"""
Using the rule of three, convert these three headline into catchy three word titles.
Do not use the same word in any of the titles.

1. {titles[0]}
2. {titles[1]}
3. {titles[2]}

Return the response as a JSON dictionary.
The JSON dictionary should have only one output entry.
The dictionary output should only have three keys as 'one', 'two' and 'three'.
Each key should have the summary of the corresponding headline.
"""


    def __message_for_model(self, titles: List[str]) -> List[Dict[str, str]]:
        """ Generate the message for the summarization model.
        """

        prompt = self.__prompt_engineered_input(titles)
        messages = [{'role': 'user', 'content': prompt}]
        return messages


    def __get_model_output(self, titles: List[str]) -> Pipeline:
        """ Get the summaries of the top news articles.
        """

        messages = self.__message_for_model(titles)
        print("Generating summaries...")
        output = self.__pipe(messages, max_length=MAX_TOKENS)
        print("Summaries generated")
        return output


    def __convert_output_to_subject(self, model_output: Pipeline) -> str:
        """ Convert the model output (JSON) to list of summaries.

        :param model_output: The model output.

        :return: The summary of the top news articles as a subject line.
        :rtype: str
        """

        # Fetch the agent response from the model output
        json_output = model_output[0]['generated_text'][-1]['content']

        # Convert the output to json compatible format
        json_output = json_output.replace('`', '')
        json_output = json_output.replace('json', '')

        # Load the json output
        json_output = json.loads(json_output)

        # Get the summary of the news articles
        summaries = [json_output[key] for key in json_output]

        # Return the summary as a concatenated string
        summary = summaries[0] + ', ' + summaries[1] + ', and ' + summaries[2]
        return summary


    def run(self) -> int:
        """ Entry point of the class.
            Sets the subject of the newsletter email.
        """

        logged_in = self.__hugging_face_login()
        if not logged_in:
            return 0

        self.__pipe = pipeline("text-generation", model=self.__model, model_kwargs={"torch_dtype": torch.bfloat16})
        titles = self.__extract_titles()
        model_output = self.__get_model_output(titles)
        self.__subject = self.__convert_output_to_subject(model_output)
        return 1


if __name__ == '__main__':
    top_news_articles = get_data('selected')['top_news']
    summarizer = TextSummarization(top_news_articles)
    summarizer.run()
    print(getattr(summarizer, '_TextSummarization__subject'))