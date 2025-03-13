import os
import httpx
from dotenv import load_dotenv
from ms_graph import get_access_token, MS_GRAPH_BASE_URL

# https://learn.microsoft.com/en-us/graph/query-parameters?tabs=http
# https://learn.microsoft.com/en-us/graph/api/resources/message?view=graph-rest-1.0#properties
# https://learn.microsoft.com/en-us/graph/api/resources/message?view=graph-rest-1.0#json-representation

def get_mails():
    load_dotenv()
    APPLICATION_ID = os.getenv('APPLICATION_ID')
    CLIENT_SECRET = os.getenv('CLIENT_SECRET')
    TENANT_ID = os.getenv('TENANT_ID')
    SCOPES = ['User.Read', 'Mail.Read']

    projects = []

    endpoint = f'{MS_GRAPH_BASE_URL}/me/messages'

    try:
        access_token = get_access_token(APPLICATION_ID, CLIENT_SECRET, SCOPES, TENANT_ID)
        headers = {
            'Authorization': access_token
        }

        for i in range(0, 4, 25):
            params = {
                '$top': 25,
                '$select': '*',
                '$skip': i,
                '$orderby': 'receivedDateTime desc'
            }

            response = httpx.get(endpoint, headers=headers, params=params)

            if response.status_code != 200:
                raise Exception(f'Failed to get emails: {response.text}')
            
            json_response = response.json()

            for mail_message in json_response.get('value', []):
                arr = mail_message['subject'].split()
                
                for a in arr:
                    if '#' in a:
                        print('Contenu', mail_message['from'])
                        print('Contenu', mail_message['uniqueBody'])
                        print('------------------')
                        if a not in projects:
                            projects.append(a)

                # print('To:', mail_message['toRecipients'])
                # print('From:', mail_message['from']['emailAddress']['name'], 
                #     f"({mail_message['from']['emailAddress']['address']})")
                # print('Is Read:', mail_message['isRead'])
                # print('Received Date Time:', mail_message['receivedDateTime'])
                print()
            return projects

    except httpx.HTTPStatusError as e:
        print(e)
    except Exception as ex:
        print(ex)

get_mails()

