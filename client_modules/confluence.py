import requests
import sys
import logging
from bs4 import BeautifulSoup

logging.getLogger(__name__)


class ConfluenceSearchResponse:
    """
    A class to represent a Confluence search response.

    Attributes
    ----------
    results : list[BlogPost]
        A list containing BlogPost objects.
    start : int
        The starting point of the search.
    limit : int
        The limit to the number of search results.
    size : int
        The actual size of the search results.
    cql : str
        The CQL (Confluence Query Language) query used for the search.
    totalSize : int
        The total size of the search result.
    searchDurationMillis : int
        The time taken for the search in milliseconds.
    self_link : str
        The link to the search result.
    """

    def __init__(self, data):
        """
        Constructs all the necessary attributes for the ConfluenceSearchResponse object.

        Parameters
        ----------
        data : dict
            The search response data from the Confluence API.
        """
        self.results: list[BlogPost] = []
        self.start = data.get(
            "start"
        )  #    start : int The starting point of the search
        self.limit = data.get("limit")
        self.size = data.get("size")
        self.cql = data.get("cql")
        self.totalSize = data.get("totalSize")
        self.searchDurationMillis = data.get("searchDurationMillis")
        self.self_link = data["_links"].get("self")

        for result in data["results"]:
            self.results.append(BlogPost(result))


class ConfluenceLinks:
    """
    A class to represent the links related to a Confluence content entity.

    Attributes
    ----------
    self_link : str
        The URL to the content entity itself.
    tinyui : str
        The URL to the tiny (shortened) UI view of the content entity.
    editui : str
        The URL to the edit UI view of the content entity.
    webui : str
        The URL to the web UI view of the content entity.
    version : str
        The URL to the version of the content entity.
    """

    def __init__(self, links_data):
        """
        Constructs all the necessary attributes for the ConfluenceLinks object.

        Parameters
        ----------
        links_data : dict
            The links data from the Confluence API.
        """
        self.self_link: str = links_data.get("self")
        self.tinyui: str = links_data.get("tinyui")
        self.editui: str = links_data.get("editui")
        self.webui: str = links_data.get("webui")
        self.version: str = links_data.get("version")


class Storage:
    """
    A class to represent the storage format of a Confluence content entity's body.

    Attributes
    ----------
    value : str
        The HTML representation of the body content.
    representation : str
        The type of the representation (usually 'storage').
    _expandable : dict
        The expandable fields for the storage object.
    """

    def __init__(self, storage_data):
        """
        Constructs all the necessary attributes for the Storage object.

        Parameters
        ----------
        storage_data : dict
            The storage data from the Confluence API.
        """
        self.value = storage_data.get("value")
        self.representation = storage_data.get("representation")
        self._expandable = storage_data.get("_expandable")


class Body:
    """
    A class to represent the body of a Confluence content entity.

    Attributes
    ----------
    storage : Storage
        The storage format of the body content.
    _expandable : dict
        The expandable fields for the body object.
    """

    def __init__(self, body_data):
        """
        Constructs all the necessary attributes for the Body object.

        Parameters
        ----------
        body_data : dict
            The body data from the Confluence API.
        """
        self.storage = Storage(body_data.get("storage"))
        self._expandable = body_data.get("_expandable")


class BlogPost:
    """
    A class to represent a BlogPost in Confluence.

    Attributes
    ----------
    id : str
        The ID of the blog post.
    type : str
        The type of the content entity (usually 'blogpost').
    status : str
        The status of the blog post (usually 'current').
    title : str
        The title of the blog post.
    extensions : dict
        Any extensions related to the blog post.
    restrictions : dict
        Any restrictions applied to the blog post.
    version : dict
        The version information of the blog post.
    metadata : dict
        The metadata of the blog post.
    operations : list
        A list of operations related to the blog post.
    _links : ConfluenceLinks
        The links related to the blog post.
    _expandable : dict
        The expandable fields for the blog post.
    body : Body
        The body of the blog post.
    """

    def __init__(self, data):
        """
        Constructs all the necessary attributes for the BlogPost object.

        Parameters
        ----------
        data : dict
            The blog post data from the Confluence API.
        """
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
        """
        Extracts the text from the body of the blog post.

        Returns
        -------
        str
            The extracted text.
        """
        soup = BeautifulSoup(self.body.storage.value, "html.parser")
        text = soup.get_text()

        return text


class ConfluenceClient:
    """
    A class that handles interactions with the Confluence API.

    Attributes
    ----------
    url : str
        The base URL for the Confluence instance.
    username : str
        The username for authentication with the Confluence instance.
    token : str
        The API token for authentication with the Confluence instance.
    """

    def __init__(self, confluence_url, confluence_username, confluence_token) -> None:
        """
        Initializes the ConfluenceClient with the necessary authentication and URL details.

        Parameters
        ----------
        confluence_url : str
            The base URL for the Confluence instance.
        confluence_username : str
            The username for authentication with the Confluence instance.
        confluence_token : str
            The API token for authentication with the Confluence instance.
        """
        self.url = confluence_url
        self.username = confluence_username
        self.token = confluence_token
        pass

    def get_blogpost(self, blogpost_id) -> BlogPost:
        """
        Retrieves a specific blog post from the Confluence instance.

        Parameters
        ----------
        blogpost_id : str
            The ID of the blogpost to retrieve.

        Returns
        -------
        BlogPost
            The retrieved BlogPost object.
        """
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
