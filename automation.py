import requests
import openai
import sys
import os
import json
from bs4 import BeautifulSoup
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import logging

logging.basicConfig(filename='logs/script_log.txt', level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def get_last_line(filename):
    try:
        with open(filename, 'rb') as f:
            f.seek(-2, 2)  # Springe zum zweitletzten Byte
            while f.read(1) != b'\n':  # Gehe rückwärts bis zum nächsten Zeilenumbruch
                f.seek(-2, 1)  # Gehe zwei Bytes zurück (eins für das gelesene Byte, eins für das nächste Byte)
            last_line = f.readline().decode()
        return last_line.strip()
    except OSError:
        logging.warning(f'Die Datei ist leer oder es gab ein Problem beim Lesen der Datei.   ( ಠ ʖ̯ ಠ)')
        return None

def get_last_blogpost(url, username, token):
    api_url = f"{url}/rest/api/content/search?cql=type%20in%20(blogpost)%20order%20by%20lastmodified%20desc&limit=1&expand=body.storage.value"
    api_url2 = f"{url}/rest/api/content/search?cql=type%20in%20(blogpost)%20order%20by%20lastmodified%20desc&limit=1&expand=history"

    response = requests.get(api_url, auth=(username, token))
    response2 = requests.get(api_url2, auth=(username, token))
    if response.status_code == 200:
        data = response.json()
        data2 = response2.json()
        if 'results' in data and len(data['results']) > 0:
            blogpost = data['results'][0]
            author = data2['results'][0]['history']['createdBy']['displayName']
            post_id = data2['results'][0]['id']

            return blogpost, post_id
    else:
        logging.error(f'Fehler beim Abrufen des letzten Blogposts. Statuscode: {response.status_code} (╯°□°）╯︵ ┻━┻')
        sys.exit(1)

    return None


def generate_summary(statement, text, api_key):
    openai.api_key = api_key

    prompt = f"{statement} {text}"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=350,
        n=1,
        stop=None,
        temperature=0.3
    )

    if 'choices' in response and len(response['choices']) > 0:
        summary = response['choices'][0]['text'].strip()
        return summary
    else:
        logging.error(f'Fehler beim Generieren der Zusammenfassung. (╯°□°）╯︵ ┻━┻')
        sys.exit(1)

    return None

def extract_text(input):
    # Create a BeautifulSoup object with the HTML content
    soup = BeautifulSoup(input, 'html.parser')

    # Extract all text from the HTML document
    text = soup.get_text()

    return text

    # Request was not successful, return None
    return None

def send_message_to_slack(text, channel):
    try:
        response = client.chat_postMessage(
          channel=channel,
          text=text)
        assert response["message"]["text"] == text
    except SlackApiError as e:
        logging.error(f"Fehler beim Senden der Nachricht an Slack: {e.response['error']}")
        sys.exit(1)

base_url = os.getenv('base_url')
confluence_username = os.getenv('confluence_username')
confluence_token = os.getenv('confluence_token')
openai_api_key = os.getenv('openai_key')
slack_token = os.getenv('slack_token')
channel = os.getenv('slack_channel')
history = 'logs/history.txt' #

blogpost , post_id, author = get_last_blogpost(base_url, confluence_username, confluence_token)
client = WebClient(token=slack_token)

last_line = get_last_line(history)

if last_line is not None:
    last_id = last_line.strip()
else:
    last_id = "0" 
    with open(history, 'a') as f:
        f.write('Anfang der Historie (☞ﾟヮﾟ)☞' + '\n')
logging.info(f'{last_id} --> {post_id}')

statement = f'Du bist Pexon und erstellst eine lockere Zusammenfassung. Fasse folgenden Text in maximal 150 Wörtern und Bulletpoints zusammen. Fange an mit "Zusammenfassung aus dem letzten Blogpost":'
#Midjourney Prompt noch nicht implementiert
#statement_prompt = f"Beschreibe mir ein simples Bild auf Englisch ohne Eigennamen welches die Keywords aus diesem Beitrag enthält mit maximal 150 Wörtern:"

if blogpost:
   if post_id != last_id:
      content = blogpost['body']['storage']['value']
      text = extract_text(content)

      logging.info("Text aus letztem Blogpost:")
      logging.info(text)
      logging.info("wird an OpenAI gesendet um eine Zusammenfassung zu erstellen. Bitte warten......")

      summary = generate_summary(statement, text, openai_api_key)
      #Midjourney Prompt noch nicht implementiert
      #prompt = generate_summary(statement_prompt, text, openai_api_key)
      if summary:
         logging.info(summary)
         logging.info(f'Zusammenfassung abgeschlossen （ ^_^）o自自o（^_^ ）')
         send_message_to_slack(summary, channel)
         logging.info(f'Zusammanfassung wurde an Slack gesendet  ~(^-^)~')
         with open(filename, 'a') as f:
            f.write(post_id + '\n')
      else:
            logging.error(f'Fehler beim Generieren der Zusammenfassung. (╯°□°）╯︵ ┻━┻')
   else:
      logging.info(f'Bereits ausgeführt. ¯\_(ツ)_/¯')
else:
    logging.warning(f'Kein Blogpost gefunden. ༼ ༎ຶ ෴ ༎ຶ༽')

