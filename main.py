#!/usr/bin/env python3
import logging
import sys
import os
from slack_client import SlackClient
import confluence
from openai_summarizer import OpenaiClient
from dotenv import load_dotenv

load_dotenv()


confluence_base_url = os.getenv("BASE_URL")
confluence_username = os.getenv("CONFLUENCE_USERNAME")
confluence_token = os.getenv("CONFLUENCE_TOKEN")
openai_api_key = os.getenv("OPENAI_API_KEY")
slack_token = os.getenv("SLACK_TOKEN")
slack_channel = os.getenv("SLACK_CHANNEL")
debug = os.getenv("DEBUG")

statement = f'Du bist Pexon und erstellst eine lockere Zusammenfassung. Fasse folgenden Text in maximal 150 Wörtern und Bulletpoints. Überschriften sollen mit einfachen "*" am anfang und ende großgeschrieben sein. Fange an mit "TL;DR:":'


logger = logging.getLogger(__name__)
logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

slackClient = SlackClient(slack_token)
confluenceClient = confluence.ConfluenceClient(
    confluence_base_url, confluence_username, confluence_token
)
last_slack_message = slackClient.get_last_summary_id(slack_channel)
openai_client = OpenaiClient(openai_api_key)

if last_slack_message != "":
    blogposts = confluenceClient.get_blogposts(20).results

    # print(blogposts[0].body.storage.value)
    logging.info(blogposts[0].extract_text())
    newer_blogposts = confluenceClient.get_blogposts_newer_than_id(
        last_slack_message, blogposts
    )

    if len(newer_blogposts) != 0:
        for post in newer_blogposts:
            logging.info(post.title)
        pass
else:
    logging.error("No scheduled messages found")

if debug:
    blogposts = confluenceClient.get_blogposts(1).results
    extracted_text = blogposts[0].extract_text()
    post_id = blogposts[0].id
    logging.info(f"Text from blogpost with id {post_id}")
    logging.info(extracted_text)
    summary = openai_client.generate_summary(statement, extracted_text)
    logging.info(f"Sumary from blogpost with id {post_id}:")
    logging.info(summary)

logging.info("last ID in Slack: " + last_slack_message)


# slack.search_message_metadata(channel)
# load env

# get messages

# get new posts
