import openai
import logging
import sys

class OpenaiClient:
    def __init__(self, openai_api_key):
        self.api_key = openai_api_key
        openai.api_key = self.api_key

    def generate_summary(self, statement: str, text: str):

        prompt = f"{statement} {text}"
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=500,
            n=1,
            stop=None,
            temperature=0.3
        )

        if 'choices' in response and len(response['choices']) > 0:
            summary = response['choices'][0]['text'].strip()
            return summary
        else:
            logging.error(f'Fehler beim Senden an Slack. (╯°□°）╯︵ ┻━┻')
            sys.exit(1)

        return None