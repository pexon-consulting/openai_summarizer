import os
import sys
import json
from datetime import datetime, timedelta
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# Create a client instance
slack_token = "xoxb-1248363883698-4318919238963-AECNjuF7lJQ9Yl88LvScMwZ0"
channel = "C05B0BRV4DA"
client = WebClient(token=slack_token)

# Define the ID
id_variable = '815693849'



def search_message_metadata(channel, id):
    latest_summery=''
    try:
        # Calculate the timestamp for one month ago
        two_month_ago = datetime.now() - timedelta(days=60)
        two_month_ago_timestamp = two_month_ago.timestamp()

        response = client.conversations_history(
            channel=channel,
            include_all_metadata=True,
            #oldest=two_month_ago_timestamp
        )
        messages = response['messages']
        for message in messages:
            if 'metadata' in message and 'event_type' in message['metadata']:
                if 'action_trigger' in message['metadata']['event_payload']:
                    if message['metadata']['event_payload']['action_trigger'] == 'sheduled':
                        latest_summery = message['metadata']['event_payload']['id']
                        break
    except SlackApiError as e:
        #logging.error(f'Fehler bei der Verbindung zu Slack {e}   ( ಠ ʖ̯ ಠ)')
        print(f'Fehler bei der Verbindung zu Slack {e}   ( ಠ ʖ̯ ಠ)')
        pass
    return latest_summery


# Beispielverwendung
print(search_message_metadata(channel, id_variable))







