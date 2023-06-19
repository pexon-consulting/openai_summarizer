import requests
import openai
import sys
import os
import json
import logging
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv
load_dotenv()


statement = f'Du bist Pexon und erstellst eine lockere Zusammenfassung. Fasse folgenden Text in maximal 150 Wörtern und Bulletpoints. Überschriften sollen mit einfachen "*" am anfang und ende großgeschrieben sein. Fange an mit "TL;DR:":'
#Midjourney Prompt noch nicht implementiert
#statement_prompt = f"Beschreibe mir ein simples Bild auf Englisch ohne Eigennamen welches die Keywords aus diesem Beitrag enthält mit maximal 150 Wörtern:"

base_url = os.getenv('base_url')
confluence_username = os.getenv('confluence_username')
confluence_token = os.getenv('confluence_token')
openai_api_key = os.getenv('openai_api_key')
slack_token = os.getenv('slack_token')
channel = os.getenv('slack_channel')
statement = f'Du bist Pexon und erstellst eine lockere Zusammenfassung. Fasse folgenden Text in maximal 150 Wörtern und Bulletpoints. Überschriften sollen mit einfachen "*" am anfang und ende großgeschrieben sein. Fange an mit "TL;DR:":'
#Midjourney Prompt noch nicht implementiert
#statement_prompt = f"Beschreibe mir ein simples Bild auf Englisch ohne Eigennamen welches die Keywords aus diesem Beitrag enthält mit maximal 150 Wörtern:"

logging.basicConfig(filename='log/script.log', level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def search_message_metadata(channel, id):
    try:
        # Calculate the timestamp for one month ago
        two_month_ago = datetime.now() - timedelta(days=60)
        two_month_ago_timestamp = two_month_ago.timestamp()

        response = client.conversations_history(
            channel=channel,
            include_metadata=True,
            oldest=two_month_ago_timestamp
        )
        messages = response['messages']

        # Search for the ID in the metadata of the messages
        id_found = False
        for message in messages:
            if 'metadata' in message and 'event_payload' in message['metadata']:
                if message['metadata']['event_type'] == id:
                    id_found = True
                    break

        if id_found:
            logging.info(f'Bereits ausgeführt. ¯\_(ツ)_/¯')
            sys.exit(1)

    except SlackApiError as e:
        logging.error(f'Fehler bei der Verbindung zu Slack {e}   ( ಠ ʖ̯ ಠ)')

def get_last_blogpost(url, username, token):
    api_url = f"{url}/rest/api/content/search?cql=type%20in%20(blogpost)%20order%20by%20lastmodified%20desc&limit=10&expand=body.storage.value"
    #api_url2 = f"{url}/rest/api/content/search?cql=type%20in%20(blogpost)%20order%20by%20lastmodified%20desc&limit=1&expand=history"

    response = requests.get(api_url, auth=(username, token))
    #response2 = requests.get(api_url2, auth=(username, token))
    if response.status_code == 200:
        data = response.json()
        #data2 = response2.json()
        if 'results' in data and len(data['results']) > 0:
            blogpost = data['results'][0]
            title = data['results'][0]['title']
            post_id = data['results'][0]['id']

            return blogpost, post_id, title
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

def extract_text(input):
    # Create a BeautifulSoup object with the HTML content
    soup = BeautifulSoup(input, 'html.parser')

    # Extract all text from the HTML document
    text = soup.get_text()

    return text

    # Request was not successful, return None
    return None

def send_message_to_slack(text, channel, id):
    try:
        response = client.chat_postMessage(
            channel=channel,
            text=text,
            metadata={
                'event_type': 'confluence_id',
                'event_payload': {
                    'id': id
                }
            }
        )
    except SlackApiError as e:
        logging.error(f"Fehler beim Senden der Nachricht an Slack: {e.response['error']}")
        sys.exit(1)

blogpost , post_id , title= get_last_blogpost(base_url, confluence_username, confluence_token)
client = WebClient(token=slack_token)
search_message_metadata(channel, post_id)
page_url = f"<{base_url}/pages/viewpage.action?pageId={post_id}|*{title}*>"

if blogpost:
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
     send_message_to_slack(page_url + "\n" + summary , channel, post_id)
     logging.info(f'Zusammanfassung wurde an Slack gesendet  ~(^-^)~')
  else:
        logging.error(f'Fehler beim Generieren der Zusammenfassung. (╯°□°）╯︵ ┻━┻')
else:
    logging.warning(f'Kein Blogpost gefunden. ༼ ༎ຶ ෴ ༎ຶ༽')

