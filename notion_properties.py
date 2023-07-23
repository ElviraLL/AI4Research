import requests
import os
from typing import List, Dict
import json

from paper import Paper
from paper_arxiv import ArxivPaper


NOTION_KEY = os.environ['NOTION_API_KEY']
class NotionProperties:
    def __init__(self):
        self.database_id = '5d51ad9214b14255b41d38fb51701e15'
        self.notion_token = NOTION_KEY
        self.headers = {
            "Authorization": "Bearer " + self.notion_token,
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }

    def create_page(self, data: Dict):
        """
        Create a page in notion with given properties
        Args:
            properties_data: dictionary of properties, refers to the notion api to construct properties data
            https://developers.notion.com/reference/property-object

        Return:
            str: page_id
        """
        create_url = "https://api.notion.com/v1/pages"
        # TODO: Add children in the content 
        payload = {"parent": {"database_id": self.database_id}, "properties": data}
        res = requests.post(create_url, headers=self.headers, json=payload)
        return res.json()

    def create_paper_page(self, paper):

        properties = {
            "Name": {"title": [{"text": {"content": paper.title}}]},
            "Link": {"url": str(paper.url)},
            "Authors": {
                "multi_select": [{'name': author} for author in paper.authors]
            },
        }
        if paper.conference:
            properties["Conference"] = {
                "select": {
                    "name": paper.conference
                }
            }
        if paper.categories:
            properties["Categories"] = {
                "multi_select": [{'name': cat} for cat in paper.categories]
            }
        res = self.create_page(properties)
        return res


    def append_block_children(self, page_id, data):
        endpoint = f"https://api.notion.com/v1/blocks/{page_id}/children"
        res = requests.patch(endpoint, headers=self.headers, json=data)
        return res.json()

    def append_paper_summary(self, page_id, summary):
        objectives = summary.get("objectives", "")
        conclusion = summary.get("conclusion", "")
        methods = summary.get("methods", "")
        body = {
            "children":[
                {
                    "object": "block",
                    "type": "table_of_contents",
                    "table_of_contents": {"color": "default"},
                },
                {
                    "object": "block",
                    "type": "heading_1",
                    "heading_1": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {
                                    "content": " Research Objectives"
                                }
                            }],
                        "color": "blue_background"},
                },
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {
                                    "content": objectives
                                }
                            }],
                    },
                },
                {
                    "object": "block",
                    "type": "heading_1",
                    "heading_1": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {
                                    "content": " Conclusion"
                                }
                            }],
                        "color": "blue_background"},
                },
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {
                                    "content": conclusion
                                }
                            }],
                    },
                },
                {
                    "object": "block",
                    "type": "heading_1",
                    "heading_1": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {
                                    "content": " Methods"
                                }
                            }],
                        "color": "blue_background"},
                },
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {
                                    "content": methods
                                }
                            }],
                    },
                },
            ]
        }
        res = self.append_block_children(page_id, body)
        return res



if __name__ == "__main__":
    notion = NotionProperties()
    authors = ["a", "b", "c"]
    author_list = [{'name': value} for value in authors]
    print(author_list)
    data = {
        "Name": {"title": [{"text": {"content": "test"}}]},
        "Link": {"url": "www.google.com"},
    }
    page = notion.create_page(data)
    print(page)

    summary = {
        "objectives": "this is the objectives",
        "conclusion": "this is the conclusion",
        "methods": "this is the methods"
    }
    res = notion.append_paper_summary(page['id'], summary)
    print(res)

