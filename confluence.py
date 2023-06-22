import requests
import logging
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

class ConfluenceSearchResponse:
    def __init__(self, data):
        self.results: list[BlogPost] = []
        self.start = data.get("start")
        self.limit = data.get("limit")
        self.size = data.get("size")
        self.base = data["_links"].get("base")
        self.context = data["_links"].get("context")
        self.self_link = data["_links"].get("self")

        print(data["results"][0])

        for result in data["results"]:
            result_obj = BlogPost()
            result_obj.id = result.get("id")
            result_obj.type = result.get("type")
            result_obj.status = result.get("status")
            result_obj.title = result.get("title")
            result_obj.childTypes = result.get("childTypes")
            result_obj.macroRenderedOutput = result.get("macroRenderedOutput")
            result_obj.restrictions = result.get("restrictions")
            result_obj._expandable = result.get("_expandable")
            result_obj._links = ConfluenceLinks(result.get("_links"))
            result_obj.body = Body(**result.get("body"))
            self.results.append(result_obj)

class ConfluenceLinks:
    def __init__(self, links_data):
        self.self_link: str = links_data.get("self")
        self.tinyui: str = links_data.get("tinyui")
        self.editui: str = links_data.get("editui")
        self.webui: str = links_data.get("webui")

class Storage:
    def __init__(self, value, representation, _expandable):
        self.value = value
        self.representation = representation
        self._expandable = _expandable

class Body:
    def __init__(self, storage, _expandable):
        self.storage = Storage(**storage)
        self._expandable = _expandable

class BlogPost:
    def __init__(self):
        self.id: str = None
        self.type = None
        self.status = None
        self.title = None
        self.childTypes = None
        self.macroRenderedOutput = None
        self.restrictions = None
        self._expandable = None
        self._links: ConfluenceLinks = None
        self.body: Body = None

    def extract_text(self):
        # Create a BeautifulSoup object with the HTML content

        soup = BeautifulSoup(self.body, 'html.parser')

        # Extract all text from the HTML document
        text = soup.get_text()

        return text

        # Request was not successful, return None
        return None



class ConfluenceClient: 
    def __init__(self, confluence_url, confluence_username, confluence_token) -> None:
        self.url = confluence_url
        self.username = confluence_username
        self.token = confluence_token
        pass

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


        api_url = f"{self.url}/rest/api/content/search?cql=type%20in%20(blogpost)%20order%20by%20created%20desc&limit={limit}&expand=body.storage"
        response = requests.get(api_url, auth=(self.username, self.token))

        search = ConfluenceSearchResponse(response.json())
        logging.info(f'Retrieved {len(search.results)} blog posts')
        return search


    def get_blogposts_newer_than_id(self, last_blogpost_id: str, blog_posts: list[BlogPost]) -> list[BlogPost]:
        
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

        logging.info(f'Found {len(newer_posts)} blog posts since last summary')
        return newer_posts






    # def get_last_blogpost(url, username, token):
    #     api_url = f"{url}/rest/api/content/search?cql=type%20in%20(blogpost)%20order%20by%20lastmodified%20desc&limit=20&expand=body.storage.value"

    #     response = requests.get(api_url, auth=(username, token))
    #     if response.status_code == 200:
    #         data = response.json()
    #         if 'results' in data and len(data['results']) > 0:
    #             blogpost = data['results'][0]
    #             title = data['results'][0]['title']
    #             post_id = data['results'][0]['id']
    #             post_url = data['results'][0]['_links']['webui']

    #             return blogpost, post_id, title, post_url
    #     else:
    #         logging.error(f'Fehler beim Abrufen des letzten Blogposts. Statuscode: {response.status_code} (╯°□°）╯︵ ┻━┻')
    #         sys.exit(1)

    #     return None

    # blogpost , post_id , title, post_url= get_last_blogpost(base_url, confluence_username, confluence_token)
    # get_last_blogpost(base_url, confluence_username, confluence_token)
    # print(f"<{base_url}{post_url}|*{title}*>")


