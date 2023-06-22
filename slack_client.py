import sys
import logging
from datetime import datetime, timedelta
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from enum import Enum

logger = logging.getLogger(__name__)

class MessageType(Enum):
    BLOGPOST_SUMMARY: str = "blogpost_summary"
    NOTIFICATION: str = "notification"

class ActionTrigger(Enum):
    SCHEDULED: str = "scheduled"
    REQUESTED: str = "requested"

class MessageMetadata:
    def __init__(self) -> None:
        self.event_type: MessageType
        self.event_payload: str

class SlackMessage:
    def __init__(self, channel, text, metadata) -> None:
        self.channel: str = channel
        self.text: str = text
        self.metadata = metadata


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
                if 'metadata' not in message or 'event_type' not in message['metadata']:
                    continue
                
                metadata = message['metadata']
                event_payload = metadata.get('event_payload', {})
                
                if event_payload.get('action_trigger') == ActionTrigger.SCHEDULED:
                    last_summary_id = event_payload.get('id')
                    break
                            
        except SlackApiError as e:
            logging.error(f"Failed to connect to Slack.  щ（ﾟДﾟщ）")
            logging.error(f"{e}")
            sys.exit(1)
        return last_summary_id


    def send_message_confluence_summary(self, text, channel, blogpost_id):
        try:
            response = self.client.chat_postMessage (
                channel=channel,
                text=text,
                metadata= {
                    'event_type': MessageType.BLOGPOST_SUMMARY,
                    'event_payload': {
                        'id': blogpost_id,
                        'action_trigger': ActionTrigger.SCHEDULED
                    }
                }
            )
            
        except SlackApiError as e:
            logging.error(f"Error sending message to Slack:  (╯°□°）╯︵ ┻━┻")
            logging.error(f"{e.response['error']}")
            sys.exit(1)


    def send_message(self, text, channel, id):
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
            logging.error(f"Error sending message to Slack:  (╯°□°）╯︵ ┻━┻")
            logging.error(f"{e.response['error']}")
            sys.exit(1)





