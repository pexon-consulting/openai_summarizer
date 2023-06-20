import openai
import logging
import sys


def generate_summary(statement, text, api_key):
    openai.api_key = api_key

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