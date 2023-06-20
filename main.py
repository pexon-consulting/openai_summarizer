import logging
import sys
import os
import slack
import confluence
import util
import openai
from dotenv import load_dotenv
load_dotenv()

base_url = os.getenv('base_url')
confluence_username = os.getenv('confluence_username')
confluence_token = os.getenv('confluence_token')
openai_api_key = os.getenv('openai_api_key')
slack_token = os.getenv('slack_token')

channel = os.getenv('slack_channel')
statement = f'Du bist Pexon und erstellst eine lockere Zusammenfassung. Fasse folgenden Text in maximal 150 Wörtern und Bulletpoints. Überschriften sollen mit einfachen "*" am anfang und ende großgeschrieben sein. Fange an mit "TL;DR:":'


logger = logging.getLogger(__name__)
logging.basicConfig(
    stream=sys.stdout, 
    level=logging.INFO, 
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


last_slack_message = slack.get_last_summary_id(channel)

if last_slack_message != "":
    blogposts = confluence.get_blogposts(base_url, confluence_username, confluence_token, 20).results
    newer_blogposts = confluence.get_blogposts_newer_than_id(last_slack_message, blogposts)

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

