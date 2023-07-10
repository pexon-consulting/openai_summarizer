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
        Generates a conversation using OpenAI's GPT-3.5 model based on the provided system message and user input.

        This function uses the "gpt-3.5-turbo-16k" model. The system message sets up the initial context of the 
        conversation, and the user message acts as an interaction with the model.

        The function logs the beginning and end of the OpenAI request. If the OpenAI API call is successful, 
        the function extracts the first choice's message content as the generated response.

        Parameters
        ----------
        system_message : str
            The initial message given by the system to set the context of the conversation.
        text : str
            The user input text to interact with the AI model.

        Returns
        -------
        str
            The generated response from the AI model. If the OpenAI API call fails, an error is logged and the 
            program is terminated.

        Raises
        ------
        SystemExit
            If the OpenAI API call does not return a choice, the function logs an error and terminates the program.
        """
        messages = [
            {"role": "system", "content": f"{system_message}"},
            {"role": "user", "content": f"{text}"},
        ]

        logging.info("Started openAI summary request")
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k",
            messages=messages,
            max_tokens=1000,
            n=1,
            stop=None,
            temperature=0.1,
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
            temperature=0.8,
        )

        logging.info("openAI summary request done")

        if "choices" in response and len(response["choices"]) > 0:
            summary = response["choices"][0]["text"].strip()
            return summary
        else:
            logging.error(f"Sending to OpenAI has failed. (╯°□°）╯︵ ┻━┻")
            sys.exit(1)
