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

    