import requests
from dotenv import load_dotenv
import os

load_dotenv()

NOTION_API_KEY = os.getenv('NOTION_API')
DATABASE_ID = os.getenv("DATABASE_ID")

def get_database_projects():
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    
    headers = {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, headers=headers)
        response.raise_for_status() 
        
        return response.json()['results']  
        
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la requête: {e}")
        return None
    

    

db_projects = []

for p in get_database_projects():
    db_projects.append(p['properties']['Name']['title'][0]['plain_text'])

