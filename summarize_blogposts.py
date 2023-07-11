#!/usr/bin/env python3
import logging
import sys
import os

import client_modules.confluence as confluence
from client_modules.slack_client import SlackClient, ActionTrigger
from client_modules.openai_summarizer import OpenaiClient

from dotenv import load_dotenv

load_dotenv()

confluence_base_url = os.getenv("BASE_URL")
confluence_username = os.getenv("CONFLUENCE_USERNAME")
confluence_token = os.getenv("CONFLUENCE_TOKEN")
openai_api_key = os.getenv("OPENAI_API_KEY")
slack_token = os.getenv("SLACK_TOKEN")
slack_channel = os.getenv("SLACK_CHANNEL")
openai_statement = os.getenv("OPENAI_STATEMENT")
debug = os.getenv("DEBUG")
requested_blogpost_id = os.getenv("REQUESTED_BLOGPOST_ID")

default_blogpost_summary_statement = '''Du bist Pexon und erstellst eine lockere Zusammenfassung. Fasse folgenden Text in maximal 150 Wörtern und Bulletpoints zusammen. 
Die nachricht sollte für slack formatiert sein.  Nutze für bulletpoints immer ein "-" am anfang der zeile. Übernimm Überschriften der sektionen, und formatiere sie fett, in dem du sie zwischen * packst, wie in diesem beispiel: *Hallo Welt*

Das ergebnis sollte so aussehen

*Überschrift*
- Bulletpoint
- Bulletpoint
- Bulletpoint
'''

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
    """
    Fetches a specific blogpost from Confluence, generates a summary using OpenAI, and posts the summary to Slack.
    The blogpost ID, blogpost summary statement, Slack channel, and Confluence base URL are assumed to be globally defined.
    """
    blogpost = confluenceClient.get_blogpost(requested_blogpost_id)

    summary = openai_client.chatCompletion(
        blogpost_summary_statement, blogpost.extract_text()
    )

    logging.info(f"Summary from blogpost with id {blogpost.id}:")

    logging.info(
        f"""Summary:  
{summary}"""
    )

    slackClient.send_message_confluence_summary(
        summary,
        blogpost.title,
        slack_channel,
        f"{confluence_base_url}{blogpost._links.tinyui}",
        blogpost.id,
        ActionTrigger.SCHEDULED.value,
    )


def test_function():
    """
    Function for testing the process of getting a blogpost, extracting text, generating a summary, and sending the summary to Slack.
    It first fetches a blogpost, logs its extracted text, generates a summary using OpenAI, logs the summary, and then sends the summary to Slack.
    It also fetches the ID of the last summary sent to Slack.
    If a summary exists, it retrieves a list of 20 blogposts and checks if there are newer blogposts than the last summary.
    If newer blogposts exist, their titles are logged.
    If no previous summary is found, it logs an error message.
    The required constants (like slack_channel, confluence_base_url, and blogpost_summary_statement) are assumed to be globally defined.
    """
    blogpost = confluenceClient.get_blogposts(1).results[0]
    extracted_text = blogpost.extract_text()
    logging.info(f"Text from blogpost with id {blogpost.id}")
    logging.info(extracted_text)
    summary = openai_client.chatCompletion(blogpost_summary_statement, extracted_text)
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
    """
    Function to fetch and summarize the newest blogposts on Confluence and post the summaries to Slack.

    It first fetches the ID of the last summary sent to Slack. If a summary exists, it retrieves a list of 20 blogposts and checks if there are
    newer blogposts than the last summary. If newer blogposts exist, it logs their IDs and titles, generates a summary using OpenAI, and then sends
    the summary to Slack. It logs an info message after each summary is sent. If no previous summary is found, it logs an error message.

    The required constants (like slack_channel, confluence_base_url, and blogpost_summary_statement) are assumed to be globally defined.
    """
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

                summary = openai_client.chatCompletion(
                    blogpost_summary_statement, post.extract_text()
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


if openai_statement:
    blogpost_summary_statement = openai_statement
else:
    blogpost_summary_statement = default_blogpost_summary_statement

if requested_blogpost_id:
    send_initial_summary()
elif debug:
    test_function()
else:
    summarize_newest_blogposts()
