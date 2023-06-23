#!/usr/bin/env python3
import logging
import sys
import os

sys.path.append("client_modules")

from slack_client import SlackClient, ActionTrigger
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

requested_blogpost_id = os.getenv("REQUESTED_BLOGPOST_ID")

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

openai_client = OpenaiClient(openai_api_key)


def send_initial_summary():
    blogpost = confluenceClient.get_blogpost(requested_blogpost_id)
    summary = openai_client.generate_summary_confluence(
        statement, blogpost.extract_text()
    )
    logging.info(f"Summary from blogpost with id {blogpost.id}:")

    slackClient.send_message_confluence_summary(
        summary,
        blogpost.title,
        slack_channel,
        f"{confluence_base_url}{blogpost._links.tinyui}",
        blogpost.id,
        ActionTrigger.SCHEDULED.value,
    )


def test_function():
    blogpost = confluenceClient.get_blogposts(1).results[0]
    extracted_text = blogpost.extract_text()
    logging.info(f"Text from blogpost with id {blogpost.id}")
    logging.info(extracted_text)
    summary = openai_client.generate_summary_confluence(statement, extracted_text)
    logging.info(f"Summary from blogpost with id {blogpost.id}:")
    logging.info(summary)

    slackClient.send_message_confluence_summary(
        summary,
        blogpost.title,
        slack_channel,
        f"{confluence_base_url}{blogpost._links.tinyui}",
        blogpost.id,
        ActionTrigger.SCHEDULED.value,
    )

    last_slack_message = slackClient.get_last_summary_id(slack_channel)

    if last_slack_message != "":
        blogposts = confluenceClient.get_blogposts(20).results

        # print(blogposts[0].body.storage.value)
        logging.info(blogposts[0].extract_text())
        newer_blogposts = confluenceClient.get_blogposts_newer_than_id(
            last_slack_message, blogposts
        )

        if len(newer_blogposts) != 0:
            for post in reversed(newer_blogposts):
                logging.info(post.title)
            pass
    else:
        logging.error("No scheduled messages found")


def summarize_newest_blogposts():
    last_slack_message = slackClient.get_last_summary_id(slack_channel)
    logging.info("last ID in Slack: " + last_slack_message)

    if last_slack_message != "":
        blogposts = confluenceClient.get_blogposts(20).results

        # print(blogposts[0].body.storage.value)
        # logging.info(blogposts[0].extract_text())
        newer_blogposts = confluenceClient.get_blogposts_newer_than_id(
            last_slack_message, blogposts
        )

        if len(newer_blogposts) != 0:
            for post in reversed(newer_blogposts):
                logging.info(post.id)
                logging.info(post.title)

                summary = openai_client.generate_summary_confluence(
                    statement, post.extract_text()
                )

                slackClient.send_message_confluence_summary(
                    summary,
                    post.title,
                    slack_channel,
                    f"{confluence_base_url}{post._links.tinyui}",
                    post.id,
                    ActionTrigger.SCHEDULED.value,
                )

                logger.info(f"Sent summary for blogpost {post.id}")

    else:
        logging.error("No scheduled messages found")


if requested_blogpost_id:
    send_initial_summary()
elif debug:
    test_function()
else:
    summarize_newest_blogposts()
