import configparser

import firebase_admin
from firebase_admin import firestore
import os
from typing import Any

from google.auth.transport.requests import Request
from google.oauth2 import id_token
import requests

import dotenv
dotenv.load_dotenv()

CURRENT_DIR=os.path.dirname(os.path.abspath(__file__))

dotenv.load_dotenv(dotenv_path="keys/keys.env")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = CURRENT_DIR + os.environ["MASTER"]

class Appsettings:
    config = configparser.ConfigParser()

    app_base_settings:dict[str, Any] = {}


    @classmethod
    def config_from_file(cls, file_path):
        cls.config.read(file_path)


        for k in cls.config["BaseSettings"]:
            cls.app_base_settings[k.upper()] = cls.config["BaseSettings"][k.upper()]
        
        if os.environ['APP'] == "PROD":
            cls.app_base_settings["BASE_FUNCTION_URL"] = cls.config["PROD"]["BASE_FUNCTION_URL"]
            
        
        elif os.environ['APP'] == "DEV":
            
            cls.app_base_settings["BASE_FUNCTION_URL"] = cls.config["DEV"]["BASE_FUNCTION_URL"]

            os.environ["FIREBASE_AUTH_EMULATOR_HOST"] = "0.0.0.0:9099"
            os.environ["FIRESTORE_EMULATOR_HOST"] = "0.0.0.0:8080"
            os.environ["STORAGE_EMULATOR_HOST"] = "http://127.0.0.1:9199"

    ...


Appsettings.config_from_file("app_config.ini")

################################################################
# THE REST OF THE PROJECT USES THESE VARIABLES
################################################################
PROJECT = Appsettings.app_base_settings["PROJECT"]
PROJECT_DOMAIN = Appsettings.app_base_settings["PROJECT_DOMAIN"]
LOCATION = Appsettings.app_base_settings["LOCATION"]
BASE_FUNCTION_URL = Appsettings.app_base_settings["BASE_FUNCTION_URL"]
################################################################



################################################################
# FOR IOS DEBUGGING
################################################################
os.environ["OBJC_DISABLE_INITIALIZE_FORK_SAFETY"]="YES"
################################################################


# firebase_admin.initialize_app(options={'storageBucket': 'daisy-dsp.appspot.com'})
firebase_admin.initialize_app(options={'projectId':PROJECT})
DB = firestore.client()

################################################################
# HELPER METHODS
################################################################
def get_id_token(function_url: str):
    # Generate a custom token for a specific UID
    auth_req = Request()
    token = id_token.fetch_id_token(auth_req, function_url)
    return token

def make_a_request(function_url: str, data: dict):
    token = get_id_token(function_url = function_url)
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-type': 'application/json'
    }
    
    response = requests.post(function_url, headers=headers, json=data)
    
    if response.status_code == 200:
        print('function call succeeded:', response.json())
        return response.json()
    else:
        print('function call failed:', response.text)