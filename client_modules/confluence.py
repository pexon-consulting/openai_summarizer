import requests
import sys
import logging
from bs4 import BeautifulSoup

logging.getLogger(__name__)


class ConfluenceSearchResponse:
    def __init__(self, data):
        self.results: list[BlogPost] = []  # results: Test
        self.start = data.get("start")
        self.limit = data.get("limit")
        self.size = data.get("size")
        self.cql = data.get("cql")
        self.totalSize = data.get("totalSize")
        self.searchDurationMillis = data.get("searchDurationMillis")
        self.self_link = data["_links"].get("self")

        for result in data["results"]:
            self.results.append(BlogPost(result))


class ConfluenceLinks:
    def __init__(self, links_data):
        self.self_link: str = links_data.get("self")
        self.tinyui: str = links_data.get("tinyui")
        self.editui: str = links_data.get("editui")
        self.webui: str = links_data.get("webui")
        self.version: str = links_data.get("version")


class Storage:
    def __init__(self, storage_data):
        self.value = storage_data.get("value")
        self.representation = storage_data.get("representation")
        self._expandable = storage_data.get("_expandable")


class Body:
    def __init__(self, body_data):
        self.storage = Storage(body_data.get("storage"))
        self._expandable = body_data.get("_expandable")


class BlogPost:
    def __init__(self, data):
        self.id: str = data.get("id")
        self.type = data.get("type")
        self.status = data.get("status")
        self.title = data.get("title")
        self.extensions = data.get("extensions")
        self.restrictions = data.get("restrictions")
        self.version = data.get("version")
        self.metadata = data.get("metadata")
        self.operations = data.get("operations")
        self._links = ConfluenceLinks(data.get("_links"))
        self._expandable = data.get("_expandable")
        self.body: Body = Body(data.get("body"))

    def extract_text(self):
        soup = BeautifulSoup(self.body.storage.value, "html.parser")
        text = soup.get_text()

        return text


class ConfluenceClient:
    def __init__(self, confluence_url, confluence_username, confluence_token) -> None:
        self.url = confluence_url
        self.username = confluence_username
        self.token = confluence_token
        pass

    def get_blogpost(self, blogpost_id) -> BlogPost:
        logging.info(f"Getting blogpost with id {blogpost_id}")
        api_url = f"{self.url}/rest/api/content/{blogpost_id}?expand=body.storage"
        response = requests.get(api_url, auth=(self.username, self.token))

        if 200 <= response.status_code < 300:
            logging.info(f"Getting blogpost with id {blogpost_id} successful")
            return BlogPost(response.json())

        else:
            logging.error("Error retrieving blogpost:")
            logging.error(response.json())
            sys.exit(1)

    def get_blogposts(self, limit) -> ConfluenceSearchResponse:
        """
        Retrieves a number of blog posts from the Confluence API.

        Parameters
        ----------
        limit : int
            The number of blog posts to retrieve.

        Returns
        -------
        ConfluenceSearchResponse
            The response from the Confluence API represented as a ConfluenceSearchResponse object.
        """

        logging.info(f"Getting latest {limit} blogposts")
        api_url = f"{self.url}/rest/api/content/search?cql=type%20in%20(blogpost)%20order%20by%20created%20desc&limit={limit}&expand=body.storage"
        response = requests.get(api_url, auth=(self.username, self.token))

        search = ConfluenceSearchResponse(response.json())
        logging.info(f"Retrieved {len(search.results)} blog posts")
        return search

    def get_blogposts_newer_than_id(
        self, last_blogpost_id: str, blog_posts: list[BlogPost]
    ) -> list[BlogPost]:
        """
        Filters the provided blog posts to those that are newer than the provided ID.

        Parameters
        ----------
        last_blogpost_id : int
            The ID of the last blog post.
        blog_posts : list[BlogPost]
            The list of blog posts to filter.

        Returns
        -------
        list[BlogPost]
            A list of blog posts that are newer than the provided ID.
        """

        newer_posts = []
        for post in blog_posts:
            if post.id == str(last_blogpost_id):
                break
            newer_posts.append(post)

        logging.info(f"Found {len(newer_posts)} blog posts since last summary")
        return newer_posts

    def get_last_blogpost(self) -> BlogPost:
        """
        Fetches the last blog post from a specified API endpoint. The API endpoint
        is determined by 'self.url' attribute of the class instance. The method
        sends a GET request to the API and expects a status code 200 for a
        successful request. If the request is successful, it returns the last
        blog post as a 'BlogPost' object. If the request fails, it logs an error
        message with the received status code and terminates the program with
        a status code of 1.

        Returns
        -------
        latest_blogpost : BlogPost
            The last blog post retrieved from the API.

        Raises
        ------
        SystemExit
            If the API request fails (i.e., if it doesn't return a 200 status code).
        """
        api_url = f"{self.url}/rest/api/content/search?cql=type%20in%20(blogpost)%20order%20by%20lastmodified%20desc&limit=20&expand=body.storage.value"

        response = requests.get(api_url, auth=(self.username, self.token))
        if response.status_code == 200:
            search = ConfluenceSearchResponse(response.json())
            latest_blogpost: BlogPost = search.results[0]

            return latest_blogpost

        else:
            logging.error(
                f"Fehler beim Abrufen des letzten Blogposts. Statuscode: {response.status_code} (╯°□°）╯︵ ┻━┻"
            )

            sys.exit(1)
