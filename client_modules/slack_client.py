import sys
import logging
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from enum import Enum
from uuid import uuid4
from typing import List

logger = logging.getLogger(__name__)

class MessageType(Enum):
    """
    Enum representing the different types of messages.

    Attributes
    ----------
    BLOGPOST_SUMMARY : str
        Represents a summary of a blogpost.
    NOTIFICATION : str
        Represents a notification.
    """

    BLOGPOST_SUMMARY: str = "blogpost_summary"
    NOTIFICATION: str = "notification"


class ActionTrigger(Enum):
    """
    Enum representing the different triggers for an action.

    Attributes
    ----------
    SCHEDULED : str
        Represents an action that is triggered based on a schedule.
    REQUESTED : str
        Represents an action that is triggered based on a request.
    """

    SCHEDULED: str = "scheduled"
    REQUESTED: str = "requested"


class MessageMetadata:
    """
    Class to hold metadata for a message.

    Attributes
    ----------
    event_type : MessageType
        The type of the event that triggered the message.
    event_payload : str
        Additional information about the event.
    """

    def __init__(self) -> None:
        self.event_type: MessageType
        self.event_payload: str


class SummaryMessage:
    """
    Class to represent a summary message.

    Attributes
    ----------
    channel : str
        The channel where the summary message is to be sent.
    text : str
        The content of the summary message.
    metadata : MessageMetadata
        The metadata associated with the summary message.
    """

    def __init__(self, channel, text, metadata) -> None:
        self.channel: str = channel
        self.text: str = text
        self.metadata = metadata


class SlackClient:
    """
    A client for interacting with Slack.

    Attributes
    ----------
    client : WebClient
        WebClient object for Slack API interaction.
    """

    def __init__(self, slack_token: str) -> None:
        self.client: WebClient = WebClient(token=slack_token)

    def get_last_summary_id(self, channel) -> str:
        """
        Fetches the id of the last summary from the specified channel.

        Parameters
        ----------
        channel : str
            The channel to fetch the last summary id from.

        Returns
        -------
        str
            The id of the last summary. If no summary is found, returns an empty string.
        """
        last_summary_id = ""
        try:
            response = self.client.conversations_history(
                channel=channel,
                include_all_metadata=True,
            )

            messages = response["messages"]

            for message in messages:
                if (
                    "metadata" not in message
                    or MessageType.BLOGPOST_SUMMARY.value
                    != message["metadata"]["event_type"]
                ):
                    continue

                metadata = message["metadata"]
                event_payload = metadata.get("event_payload", {})

                if event_payload.get("action_trigger") == ActionTrigger.SCHEDULED.value:
                    last_summary_id = event_payload.get("id")
                    break

        except SlackApiError as e:
            logging.error(f"Failed to connect to Slack.  щ（ﾟДﾟщ）")
            logging.error(f"{e}")
            sys.exit(1)
        return last_summary_id

    def send_message_confluence_summary(
        self,
        summary,
        title,
        channel,
        blogpost_url,
        blogpost_id,
        actiontrigger,
    ):
        """
        Sends a message to the specified channel containing the summary of a confluence post.

        Parameters
        ----------
        summary : str
            The summary of the confluence post.
        title : str
            The title of the confluence post.
        channel : str
            The channel to send the message to.
        blogpost_url : str
            The URL of the blogpost.
        blogpost_id : str
            The ID of the blogpost.
        actiontrigger : str
            The action trigger for the event.
        """
        block_sections = []

        sections = split_sections_by_blank_lines(summary)
        for section in sections:
            block_sections.append({
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"{ section }"},
            })
            
        try:
            blocks = [
                {"type": "header", "text": {"type": "plain_text", "text": title}},
                {
                    "type": "section",
                    "text": {"type": "mrkdwn", "text": f"*TL;DR:*"},
                },
            ]
            blocks.extend(block_sections)
            blocks.append(
                {
                    "type": "actions",
                    "elements": [
                        {
                            "type": "button",
                            "text": {"type": "plain_text", "text": "Open blog post"},
                            "url": blogpost_url,
                        }
                    ],
                },
            )

            logging.debug("Blocks:")
            logging.debug(blocks)
            logging.debug("Blocks:")
            response = self.client.chat_postMessage(
                channel=channel,
                blocks=blocks,
                metadata={
                    "event_type": MessageType.BLOGPOST_SUMMARY.value,
                    "event_payload": {
                        "id": blogpost_id,
                        "action_trigger": actiontrigger,
                    },
                },
            )

            if 200 <= response.status_code < 300:
                logger.info(
                    f"Successfully sent Slack { MessageType.BLOGPOST_SUMMARY.value } message with blogpost_id: {blogpost_id}"
                )

        except SlackApiError as e:
            logging.error(f"Error sending message to Slack:  (╯°□°）╯︵ ┻━┻")
            logging.error(f"{e.response['error']}")
            sys.exit(1)

def split_sections_by_blank_lines(text):
    """
    Splits a given text into sections based on blank lines.

    This function splits the input text into sections wherever it finds one or more blank lines. The blank lines act as delimiters 
    between different sections of the text.

    Parameters
    ----------
    text : str
        The input text to be split into sections.

    Returns
    -------
    List[str]
        A list of text sections extracted from the input. Each item in the list represents a distinct section from the input text.
    """
    return [section for section in text.split('\n\n')]
