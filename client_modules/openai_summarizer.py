import openai
import logging
import sys

logging.getLogger(__name__)


class OpenaiClient:
    def __init__(self, openai_api_key):
        self.api_key = openai_api_key
        openai.api_key = self.api_key

    def generate_summary_confluence(self, statement: str, text: str) -> str:
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
