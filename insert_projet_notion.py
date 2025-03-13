import requests
from dotenv import load_dotenv
import os
from get_emails import get_mails
from get_projects import db_projects

load_dotenv()

projects = get_mails()

NOTION_API_KEY = os.getenv('NOTION_API')
DATABASE_ID = os.getenv("DATABASE_ID")

headers = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

for project in projects:
    
    if not project in db_projects:
        data = {
        "parent": {
            "database_id": DATABASE_ID
        },
        "properties": {
            "Name": {
            "title": [
                {
                "text": {
                    "content": project
                }
                }
            ]
            }
        },
        "children": [
            {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [
                {
                    "type": "text",
                    "text": {
                    "content": "Voici mon texte personnalisé"
                    }
                }
                ]
            }
            }
        ]
        }
        response = requests.post("https://api.notion.com/v1/pages", json=data, headers=headers)
    else:
        print('Projet déjà existant')