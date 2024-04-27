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