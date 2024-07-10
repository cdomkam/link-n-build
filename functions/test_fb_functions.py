import google.auth
from google.auth.transport.requests import Request
import requests
# import json
# import firebase_admin
from firebase_admin import auth
import os
import dotenv

CURRENT_DIR=os.path.dirname(os.path.abspath(__file__))

dotenv.load_dotenv(dotenv_path="keys/keys.env")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = CURRENT_DIR + os.environ["GEM_KEYS_FUNCTION"]



def get_id_token(func: str):
    # Generate a custom token for a specific UID
    auth_req = Request()
    token = google.oauth2.id_token.fetch_id_token(auth_req, func)
    return token


def call_firebase_function(function_url, data):

    
    token = get_id_token(func = function_url)
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-type': 'application/json'
    }

    response = requests.post(function_url, headers=headers, json=data)
    
    if response.status_code == 200:
        print('function call succeeded:', response.json())
    else:
        print('function call failed:', response.text)

if __name__ == "__main__":
    # function_url = 'https://<region>-<project>.cloudfunctions.net/func_name'
    # function_url = 'https://us-central1-gemini-team.cloudfunctions.net/say_hello'
    # function_url = 'https://say-hello-anj2hgg54a-uc.a.run.app'
    # function_url = 'http://localhost:5001/gemini-team/us-central1/say_hello'
    function_url = 'http://localhost:5001/gemini-team/us-central1/add_conversation'
    data={
            "comment":"this is my comment",
            "response":"this is my response",
            "user_id":"c1dbf4a1-b2af-4423-9c07-2d9a98806ff5"
    }
    
    call_firebase_function(function_url, data)