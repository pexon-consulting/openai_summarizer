#!/usr/bin/env python3
import logging
import sys
import os
from slack import SlackClient
import confluence
from dotenv import load_dotenv
load_dotenv()


confluence_base_url = os.getenv('BASE_URL')
confluence_username = os.getenv('CONFLUENCE_USERNAME')
confluence_token = os.getenv('CONFLUENCE_TOKEN')
openai_api_key = os.getenv('OPENAI_API_KEY')
slack_token = os.getenv('SLACK_TOKEN')

slack_channel = os.getenv('SLACK_CHANNEL')
statement = f'Du bist Pexon und erstellst eine lockere Zusammenfassung. Fasse folgenden Text in maximal 150 Wörtern und Bulletpoints. Überschriften sollen mit einfachen "*" am anfang und ende großgeschrieben sein. Fange an mit "TL;DR:":'


logger = logging.getLogger(__name__)
logging.basicConfig(
    stream=sys.stdout, 
    level=logging.INFO, 
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

slackClient = SlackClient(slack_token)
confluenceClient = confluence.ConfluenceClient(confluence_base_url, confluence_username, confluence_token)
last_slack_message = slackClient.get_last_summary_id(slack_channel)

if last_slack_message != "":
    blogposts = confluenceClient.get_blogposts(20).results
    newer_blogposts = confluenceClient.get_blogposts_newer_than_id(last_slack_message, blogposts)

    if len(newer_blogposts) != 0:
        for post in newer_blogposts:
            print(post.title)
        pass
else:
    print("No scheduled messages found")

print(last_slack_message)



#slack.search_message_metadata(channel)
# load env

# get messages

# get new posts

