import sys
import logging
from datetime import datetime, timedelta
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


logger = logging.getLogger(__name__)

class SlackClient:

    def __init__(self, slack_token: str) -> None:
        self.client: WebClient = WebClient(token=slack_token)

    def get_last_summary_id(self, channel) -> str:
        last_summary_id = ""
        try:
            response = self.client.conversations_history(
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
            logging.error(f"Failed to connect to Slack.")
            logging.error(f"{e}")
            sys.exit(1)
        return last_summary_id


    def send_message_to_slack(self, text, channel, id):
        try:
            response = self.client.chat_postMessage (
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
            logging.error(f"Error sending message to Slack:")
            logging.error(f"{e.response['error']}")
            sys.exit(1)





