import feedparser
from typing import List
import requests
from bs4 import BeautifulSoup
from dateutil import parser


class FeedItem:
    """
    Class for creating and managing feed items.

    Parameters
    ----------
    title : str
        The title of the feed item.
    link : str
        The URL of the feed item.
    comments : str
        The comments associated with the feed item.
    creator : str
        The creator of the feed item.
    pub_date : str
        The publication date of the feed item.
    category : str
        The category of the feed item.
    guid : str
        The globally unique identifier of the feed item.
    description : str
        The description of the feed item.
    content_encoded : str
        The encoded content of the feed item.
    comment_rss : str
        The comment RSS of the feed item.
    num_comments : str
        The number of comments on the feed item.
    """

    def __init__(
        self,
        title,
        link,
        comments,
        creator,
        pub_date,
        category,
        guid,
        description,
        content_encoded,
        comment_rss,
        num_comments,
    ):
        self.title = title
        self.link = link.strip()  # Remove newline characters
        self.comments = comments.strip()  # Remove newline characters
        self.creator = creator
        self.pub_date = pub_date
        self.category = category
        self.guid = guid
        self.description = description
        self.content_encoded = content_encoded
        self.comment_rss = comment_rss.strip()  # Remove newline characters
        self.num_comments = num_comments
        self.parsed_date = parser.parse(pub_date)

    def extract_blog_text(self) -> str:
        """
        Extracts the blog text from the feed item's link.

        Returns
        -------
        str
            The extracted blog text.
        """
        url = self.link
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        # Select the specific div using its XPath
        specific_div = soup.select("body > main > div > div:nth-of-type(2)")

        for ul in specific_div[0].find_all("ul"):
            ul.decompose()

        # Extract the text within the div
        raw_text = specific_div[0].get_text(separator="\n")

        # Split the text into lines, filter out the empty lines, and join the lines back together
        blog_text = "\n".join(
            line
            for line in raw_text.split("\n")
            if line.strip()
            and line.strip() not in ["Additional resources:", "Related Products"]
        )

        return blog_text


class FeedChannel:
    """
    Class for creating and managing feed channels.

    Parameters
    ----------
    title : str
        The title of the feed channel.
    atom_link : str
        The atom link of the feed channel.
    link : str
        The link to the feed channel.
    description : str
        The description of the feed channel.
    last_build_date : str
        The last build date of the feed channel.
    language : str
        The language of the feed channel.
    update_period : str
        The update period of the feed channel.
    update_frequency : str
        The update frequency of the feed channel.
    generator : str
        The generator of the feed channel.
    """

    def __init__(
        self,
        title,
        atom_link,
        link,
        description,
        last_build_date,
        language,
        update_period,
        update_frequency,
        generator,
    ):
        self.title = title
        self.atom_link = atom_link
        self.link = link
        self.description = description
        self.last_build_date = last_build_date
        self.language = language
        self.update_period = update_period.strip()  # Remove newline characters
        self.update_frequency = update_frequency.strip()  # Remove newline characters
        self.generator = generator
        self.items: List[FeedItem] = []  # List of FeedItem objects

    def add_item(self, item):
        """
        Adds a feed item to the feed channel.

        Parameters
        ----------
        item : FeedItem
            The feed item to add.
        """
        if isinstance(item, FeedItem):
            self.items.append(item)


def create_channel(feed_url) -> FeedChannel:
    """
    Creates a FeedChannel object from a provided feed URL.

    Parameters
    ----------
    feed_url : str
        The URL of the feed.

    Returns
    -------
    FeedChannel
        The created FeedChannel object.
    """
    feed = feedparser.parse(feed_url)

    # Define defaults for missing values
    defaults = {
        "last_build_date": "N/A",
        "language": "N/A",
        "update_period": "N/A",
        "update_frequency": "N/A",
        "generator": "N/A",
    }

    # Use the parsed feed data if available, otherwise use the default values
    channel = FeedChannel(
        title=feed.feed.title,
        atom_link=feed.feed.links[0].href if feed.feed.links else "N/A",
        link=feed.feed.link,
        description=feed.feed.description,
        last_build_date=getattr(feed.feed, "updated", defaults["last_build_date"]),
        language=getattr(feed.feed, "language", defaults["language"]),
        update_period=getattr(feed.feed, "sy_updateperiod", defaults["update_period"]),
        update_frequency=getattr(
            feed.feed, "sy_updatefrequency", defaults["update_frequency"]
        ),
        generator=getattr(feed.feed, "generator_detail", defaults["generator"]),
    )

    for entry in feed.entries:
        item = FeedItem(
            title=entry.title,
            link=entry.link,
            comments=getattr(entry, "comments", "N/A"),
            creator=getattr(entry, "dc_creator", "N/A"),
            pub_date=entry.published,
            category=getattr(entry, "category", "N/A"),
            guid=getattr(entry, "guid", "N/A"),
            description=getattr(entry, "description", "N/A"),
            content_encoded=getattr(entry, "content_encoded", "N/A"),
            comment_rss=getattr(entry, "wfw_commentrss", "N/A"),
            num_comments=getattr(entry, "slash_comments", "N/A"),
        )
        channel.add_item(item)

    return channel
