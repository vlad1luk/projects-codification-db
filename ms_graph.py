import os
import webbrowser
import msal
from dotenv import load_dotenv

MS_GRAPH_BASE_URL = 'https://graph.microsoft.com/v1.0'


def get_access_token(application_id, client_secret, scopes, tenant_id):
    client = msal.ConfidentialClientApplication(
        client_id=application_id,
        client_credential=client_secret,
        authority=f'https://login.microsoftonline.com/{tenant_id}',
    )                                       

    refresh_token = None

    if os.path.exists('refresh_token.txt'):
        with open('refresh_token.txt', 'r') as file:
            refresh_token = file.read().strip()
    
    if refresh_token:
        token_response = client.acquire_token_by_refresh_token(refresh_token, scopes)
    else:
        auth_request_url = client.get_authorization_request_url(scopes)
        webbrowser.open(auth_request_url)
        authorization_code = input('Enter the authorization code: ')

        if not authorization_code:
            return ValueError('Authorization Code is Empty')
        
        token_response = client.acquire_token_by_authorization_code(
            code=authorization_code,
            scopes=scopes
        )

    if 'access_token' in token_response:
        if 'refresh_token' in token_response:
            with open('refresh_token.txt', 'w') as file:
                file.write(token_response['refresh_token'])
        return token_response['access_token']
    else:
        raise Exception('Failed to acquire token:' + str(token_response))
    
def main():
    load_dotenv()
    APPLICATION_ID = os.getenv('APPLICATION_ID')
    CLIENT_SECRET = os.getenv('CLIENT_SECRET')
    TENANT_ID = os.getenv('TENANT_ID')
    SCOPES = ['User.Read', 'Mail.Read']

    try:
        access_token = get_access_token(APPLICATION_ID, CLIENT_SECRET, SCOPES, TENANT_ID)
        headers = {
            'Authorization': f'Bearer {access_token}'
        }

    except Exception as ex:
        print(ex)

main()