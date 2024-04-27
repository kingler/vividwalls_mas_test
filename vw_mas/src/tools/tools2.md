notion_api_tools-v2.py
```python
import requests
from langchain.tools import tool
import logging

class NotionTools:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.notion.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28",
        }

    # ... (existing methods remain the same)

    @tool("Create Campaign Project")
    def create_campaign_project(self, title: str, description: str, properties: dict) -> str:
        """
        Creates a new campaign project in Notion.
        :param title: The title of the campaign project.
        :param description: The description of the campaign project.
        :param properties: Additional properties for the campaign project.
        :return: The ID of the newly created campaign project.
        """
        url = f"{self.base_url}/pages"
        data = {
            "parent": {"database_id": "your_ad_campaign_database_id"},
            "properties": {
                "Name": {"title": [{"text": {"content": title}}]},
                "Description": {"rich_text": [{"text": {"content": description}}]},
                **properties
            }
        }
        response = requests.post(url, headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()["id"]

    @tool("Update Campaign Project")
    def update_campaign_project(self, project_id: str, properties: dict) -> None:
        """
        Updates a campaign project in Notion.
        :param project_id: The ID of the campaign project to update.
        :param properties: The properties to update in the campaign project.
        """
        url = f"{self.base_url}/pages/{project_id}"
        data = {"properties": properties}
        response = requests.patch(url, headers=self.headers, json=data)
        response.raise_for_status()

    @tool("Create Artifact Page")
    def create_artifact_page(self, parent_page_id: str, title: str, content: list) -> str:
        """
        Creates a new artifact page in Notion.
        :param parent_page_id: The ID of the parent page for the artifact.
        :param title: The title of the artifact page.
        :param content: The content blocks for the artifact page.
        :return: The ID of the newly created artifact page.
        """
        url = f"{self.base_url}/pages"
        data = {
            "parent": {"page_id": parent_page_id},
            "properties": {
                "title": {"title": [{"text": {"content": title}}]}
            },
            "children": content
        }
        response = requests.post(url, headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()["id"]

    def handle_error(self, error: Exception) -> None:
        """
        Handles errors that occur during Notion API interactions.
        :param error: The error exception.
        """
        logging.error(f"Notion API Error: {str(error)}")
        # Additional error handling logic

    def authenticate(self) -> None:
        """
        Performs authentication with the Notion API.
        """
        # Include Authentication logic using the Notion API key

    # Include any additional methods (e.g., other updated methods)
```

notion_api_tool.py
```python
import requests
from langchain.tools import tool

class NotionTools:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.notion.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28",
        }

    # ... (existing methods remain the same)

    @tool("Append Block Children")
    def append_block_children(self, block_id: str, children: list, after: str = None) -> dict:
        """
        Appends new children blocks to a specified parent block.
        :param block_id: The ID of the parent block.
        :param children: An array of child block objects to append.
        :param after: (Optional) The ID of the block to append the new children after.
        :return: A dictionary containing the newly created child block objects.
        """
        url = f"{self.base_url}/blocks/{block_id}/children"
        data = {"children": children}
        if after:
            data["after"] = after
        response = requests.patch(url, headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()

    @tool("Retrieve Block")
    def retrieve_block(self, block_id: str) -> dict:
        """
        Retrieves a block object using the specified block ID.
        :param block_id: The ID of the block to retrieve.
        :return: A dictionary containing the retrieved block object.
        """
        url = f"{self.base_url}/blocks/{block_id}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    @tool("Retrieve Block Children")
    def retrieve_block_children(self, block_id: str, start_cursor: str = None, page_size: int = 100) -> dict:
        """
        Retrieves a paginated array of child block objects for the specified parent block.
        :param block_id: The ID of the parent block.
        :param start_cursor: (Optional) The cursor to start the pagination from.
        :param page_size: (Optional) The number of items to return per page (max 100).
        :return: A dictionary containing the paginated child block objects.
        """
        url = f"{self.base_url}/blocks/{block_id}/children"
        params = {"page_size": page_size}
        if start_cursor:
            params["start_cursor"] = start_cursor
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()

    @tool("Update Block")
    def update_block(self, block_id: str, block_data: dict) -> dict:
        """
        Updates the content of a specified block based on its type.
        :param block_id: The ID of the block to update.
        :param block_data: A dictionary containing the updated block data.
        :return: A dictionary containing the updated block object.
        """
        url = f"{self.base_url}/blocks/{block_id}"
        response = requests.patch(url, headers=self.headers, json=block_data)
        response.raise_for_status()
        return response.json()

    @tool("Delete Block")
    def delete_block(self, block_id: str) -> None:
        """
        Archives a block using the specified block ID.
        :param block_id: The ID of the block to delete (archive).
        """
        url = f"{self.base_url}/blocks/{block_id}"
        response = requests.delete(url, headers=self.headers)
        response.raise_for_status()
```

notion_tool.py
```python
from langchain.tools import tool
import requests

@tool("Comprehensive Notion API Interaction")
class NotionTool:
    """This tool interfaces with all major aspects of the Notion API, including managing databases, pages, blocks, and user interactions. It supports creating, updating, querying, and deleting data within Notion workspaces."""

    def __init__(self, notion_token):
        self.notion_token = notion_token
        self.headers = {
            "Authorization": f"Bearer {self.notion_token}",
            "Notion-Version": "2021-05-13",
            "Content-Type": "application/json"
        }

    def create_or_update_page(self, database_id, page_data):
        url = f"https://api.notion.com/v1/pages"
        data = {
            "parent": {"database_id": database_id},
            "properties": page_data
        }
        response = requests.post(url, headers=self.headers, json=data)
        return response.json()

    def retrieve_page(self, page_id):
        url = f"https://api.notion.com/v1/pages/{page_id}"
        response = requests.get(url, headers=self.headers)
        return response.json()

    def update_page_properties(self, page_id, properties):
        url = f"https://api.notion.com/v1/pages/{page_id}"
        data = {"properties": properties}
        response = requests.patch(url, headers=self.headers, json=data)
        return response.json()

    def query_database(self, database_id, filter, sort):
        url = f"https://api.notion.com/v1/databases/{database_id}/query"
        data = {"filter": filter, "sorts": sort}
        response = requests.post(url, headers=self.headers, json=data)
        return response.json()

    def create_database(self, parent_page_id, title, properties):
        url = f"https://api.notion.com/v1/databases"
        data = {
            "parent": {"page_id": parent_page_id},
            "title": title,
            "properties": properties
        }
        response = requests.post(url, headers=self.headers, json=data)
        return response.json()   
```
Analyze the three notion api python files in the tools directory. Identify how they can be combined to provide the ability to read, create, update, and delete content in a notion database.  