import openai
import logging
import sys

logging.getLogger(__name__)


class OpenaiClient:
    """
    A class to interface with OpenAI's API.

    Attributes
    ----------
    api_key : str
        The API key for OpenAI.
    """

    def __init__(self, openai_api_key):
        """
        Initializes the OpenaiClient with the provided API key.

        Parameters
        ----------
        openai_api_key : str
            The API key for OpenAI.
        """
        self.api_key = openai_api_key
        openai.api_key = self.api_key

    def chatCompletion(self, system_message: str, text: str) -> str:
        """
        Generates a summary using OpenAI's GPT-3 model based on the provided statement and text.

        Parameters
        ----------
        statement : str
            The initial statement to start the summary with.
        text : str
            The text to summarize.

        Returns
        -------
        str
            The generated summary.
        """
        messages = [
            {"role": "system", "content": f"{system_message}"},
            {"role": "user", "content": f"{text}"},
        ]

        logging.info("Started openAI summary request")
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=500,
            n=1,
            stop=None,
            temperature=0.8,
        )

        logging.info("openAI summary request done")

        if "choices" in response and len(response["choices"]) > 0:
            summary = response["choices"][0]["message"]["content"].strip()
            return summary
        else:
            logging.error(f"Sending to OpenAI has failed. (╯°□°）╯︵ ┻━┻")
            sys.exit(1)

    def generate_summary_confluence(self, statement: str, text: str) -> str:
        """
        Generates a summary using OpenAI's GPT-3 model based on the provided statement and text.

        Parameters
        ----------
        statement : str
            The initial statement to start the summary with.
        text : str
            The text to summarize.

        Returns
        -------
        str
            The generated summary.
        """
        prompt = f"{statement} {text}"

        logging.info("Started openAI summary request")
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=500,
            n=1,
            stop=None,
            temperature=0.3,
        )

        logging.info("openAI summary request done")

        if "choices" in response and len(response["choices"]) > 0:
            summary = response["choices"][0]["text"].strip()
            return summary
        else:
            logging.error(f"Sending to OpenAI has failed. (╯°□°）╯︵ ┻━┻")
            sys.exit(1)
