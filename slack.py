import os
import sys
import logging
from datetime import datetime, timedelta
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv
load_dotenv()

logger = logging.getLogger(__name__)
slack_token = os.getenv('slack_token')
channel = os.getenv('slack_channel')

client = WebClient(token=slack_token)

def get_last_summary_id(channel) -> str:
    last_summary_id = ""
    try:
        response = client.conversations_history(
            channel=channel,
            include_all_metadata=True,
        )

        messages = response['messages']
        for message in messages:
            if 'metadata' in message and 'event_type' in message['metadata']:
                if 'action_trigger' in message['metadata']['event_payload']:
                    if message['metadata']['event_payload']['action_trigger'] == 'sheduled':
                        last_summary_id = message['metadata']['event_payload']['id']
                        break
                        
    except SlackApiError as e:
        logging.error(f'Fehler bei der Verbindung zu Slack {e}   ( ಠ ʖ̯ ಠ)')
        #print(f'Fehler bei der Verbindung zu Slack {e}   ( ಠ ʖ̯ ಠ)')
        pass
    return last_summary_id



def send_message_to_slack(text, channel, id):
    try:
        response = client.chat_postMessage (
            channel=channel,
            text=text,
            metadata= {
                'event_type': 'confluence_id',
                'event_payload': {
                    'id': id,
                    'action_trigger': "sheduled"
                }
            }
        )
        
    except SlackApiError as e:
        logging.error(f"Fehler beim Senden der Nachricht an Slack: {e.response['error']}")
        sys.exit(1)





