from langchain.tools import tool
import requests

@tool("Comprehensive Notion API Interaction")
class NotionTool:
    """This tool interfaces with all major aspects of the Notion API, including managing databases, 
pages, blocks, and user interactions. It supports creating, updating, querying, and deleting data 
within Notion workspaces."""

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

    def append_blocks_to_page(self, page_id, blocks):
        """
        Appends blocks to a page in Notion.
        :param page_id: The ID of the page to append blocks to.
        :param blocks: A list of block objects to append.
        """
        url = f"https://api.notion.com/v1/blocks/{page_id}/children"
        data = {"children": blocks}
        response = requests.patch(url, headers=self.headers, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to append blocks: {response.text}")
