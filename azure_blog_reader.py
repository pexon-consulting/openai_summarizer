#!/usr/bin/env python3

from os import getenv
import logging
import sys
from client_modules.slack_client import SlackClient
from client_modules.openai_summarizer import OpenaiClient
from client_modules.azure_feedreader import create_channel
from dotenv import load_dotenv
from datetime import datetime
from dateutil import parser

load_dotenv()

logger = logging.getLogger(__name__)
logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


client = OpenaiClient(getenv("OPENAI_API_KEY"))
slackClient = SlackClient(getenv("SLACK_TOKEN"))
slack_channel = getenv("SLACK_CHANNEL")
default_statement = 'You are a consultant for a Cloud consulting company. You are reading the Azure blog for new Features of the azure cloud platform. Gather the key points of the post, and create a summary using 150 words or less, and use bullet points where appropriate. Write from the perspective of "Azure announced" or "Azure posted on their blog". Also generate a heading, and dont include the Release date of the update post. Also do not include phrases that say things like "You can find more info one another page"'
azure_rss_url = getenv("AZURE_RSS_URL")

debug_date = "Wed, 29 Mar 2023 17:01:20 Z"

custom_statement = getenv("CUSTOM_AZURE_STATEMENT")

statement: str

if custom_statement:
    statement = custom_statement
else:
    statement = default_statement


def send_azure_summary():
    channel = create_channel(
        "https://azure.microsoft.com/de-de/updates/feed/?category=compute%2Ccontainers%2Cdatabases%2Cdevops%2Cai-machine-learning%2Cnetworking%2Csecurity%2Cstorage&status=nowavailable%2Cinpreview"
    )

    post = channel.items[0]
    extracted_text = post.extract_blog_text()

    print(
        f"""RAW TEXT

    {extracted_text}


    """
    )

    summary = client.chatCompletion(statement, extracted_text)
    print(
        f"""Summarized text

    {summary}


    """
    )

    slackClient.send_azure_blogpost_summary(
        post.title, summary, post.link, getenv("SLACK_CHANNEL"), post.pub_date
    )


channel = create_channel(
    "https://azure.microsoft.com/de-de/updates/feed/?category=compute%2Ccontainers%2Cdatabases%2Cdevops%2Cai-machine-learning%2Cnetworking%2Csecurity%2Cstorage&status=nowavailable%2Cinpreview"
)


for post in channel.items:
    today = datetime.now().date() if not debug_date else parser.parse(debug_date).date()

    # print(today)

    # if today == post.parsed_date.date():
    #     print(True)
    # else:
    #     print(False)
    # print(post.title)
    print(post.parsed_date.date())


print(slackClient.get_last_azure_summary_date(slack_channel))
# if __name__ == "__main__":
#     send_azure_summary()
