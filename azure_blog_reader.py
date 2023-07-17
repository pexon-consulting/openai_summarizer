#!/usr/bin/env python3

import logging
import sys
from collections import defaultdict
from os import getenv
from typing import List

from dateutil import parser
from dotenv import load_dotenv

from client_modules.azure_feedreader import FeedItem, create_channel
from client_modules.openai_summarizer import OpenaiClient
from client_modules.slack_client import SlackClient

load_dotenv()

logger = logging.getLogger(__name__)
logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

openai_client = OpenaiClient(getenv("OPENAI_API_KEY"))
slackClient = SlackClient(getenv("SLACK_TOKEN"))
slack_channel = getenv("SLACK_CHANNEL")

default_system_message = """ You are a consultant for a Cloud consulting company. You are reading the Azure blog for new Features of the azure cloud platform. Gather the key points of each section, and create a summary using 150 words or less for each one, and use bullet points where appropriate. Write from the perspective of "Azure announced" or "Azure posted on their blog". Also generate a heading, and dont include the Release date of the update post. Also do not include phrases that say things like "You can find more info one another page.

Your output will be output to Slack, which supports a special form of markdown. * around text makes it bold, - indicate a bulleted list. 

Slack does not use Markdown links. The format for links is as follows:
<http://www.example.com|Heading>


In your input, each section is separated by ---, and contains the fields Heading, Link, and Blog Content.

Take these sections, take the fields and output the summarized sections like this. Separate each section using ---. Replace http://www.example.com with the link in the section:

*Heading*
- Bulletpoint
- Bulletpoint
- Bulletpoint

<http://www.example.com|Read more>

---
"""

azure_rss_url = getenv("AZURE_RSS_URL")
custom_system_message = getenv("AZURE_SYSTEM_MESSAGE")

system_message: str

if custom_system_message:
    system_message = custom_system_message
else:
    system_message = default_system_message


def summarize_day(groups, date):
    """
    Summarizes all the Azure blog posts for a particular day and posts them to Slack.

    Parameters
    ----------
    groups : dict
        The dictionary of blog posts grouped by day.
    date : datetime.date
        The date for which to summarize blog posts.
    """

    day = groups[date]

    contents = ""

    for item in day:
        contents = f"""{ contents }

Heading: { item.title }

Link: { item.link }

Blog Content:

{ item.extract_blog_text() }

___
"""

    summary = openai_client.chatCompletion(system_message, contents)
    sections = summary.split("---")
    slackClient.send_azure_blogpost_summary(sections, slack_channel, str(date))


def summarize_newer_groups(groups, last_date):
    """
    Summarizes all the Azure blog posts for days later than a particular date and posts them to Slack.

    Parameters
    ----------
    groups : dict
        The dictionary of blog posts grouped by day.
    last_date : datetime.date
        The date to use as a reference point.
    """

    keys = groups.keys()

    date_list = list(keys)

    new_dates = []

    # Loop over the groups
    for date in date_list:
        # Check whether the date is later than the input date
        if date > last_date:
            new_dates.append(date)

            # If it is, print the date and the number of items
            print(f"Date: {date}, Item count: {len(groups[date])}")
            summarize_day(groups, date)
        elif date < last_date:
            break

    for date in reversed(new_dates):
        print(f"Date: {date}, Item count: {len(groups[date])}")
        summarize_day(groups, date)


def latest_posts():
    """
    Retrieves the latest blog posts from the Azure blog and summarizes them.
    """

    channel = create_channel(
        "https://azure.microsoft.com/de-de/updates/feed/?category=compute%2Ccontainers%2Cdatabases%2Cdevops%2Cai-machine-learning%2Cnetworking%2Csecurity%2Cstorage&status=nowavailable%2Cinpreview"
    )

    last_date = parser.parse(
        slackClient.get_last_azure_summary_date(slack_channel)
    ).date()

    summarize_newer_groups(channel.groups, last_date)


def specific_day():
    """
    Summarizes the Azure blog posts for a specific day set by the 'AZURE_SUMMARY_DATE' environment variable.
    """

    channel = create_channel(
        "https://azure.microsoft.com/de-de/updates/feed/?category=compute%2Ccontainers%2Cdatabases%2Cdevops%2Cai-machine-learning%2Cnetworking%2Csecurity%2Cstorage&status=nowavailable%2Cinpreview"
    )

    date = getenv("AZURE_SUMMARY_DATE")

    summarize_day(channel.groups, parser.parse(date).date())


if getenv("AZURE_SUMMARY_DATE"):
    specific_day()
else:
    summarize_newer_groups()
