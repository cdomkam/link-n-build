import configparser

import firebase_admin
from firebase_admin import firestore
import os
from typing import Any

import dotenv
dotenv.load_dotenv()

# CURRENT_DIR=os.path.dirname(os.path.abspath(__file__))
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = CURRENT_DIR + "/daisy-dsp-firebase-adminsdk.json"

class Appsettings:
    config = configparser.ConfigParser()

    app_base_settings:dict[str, Any] = {}


    @classmethod
    def config_from_file(cls, file_path):
        cls.config.read(file_path)


        for k in cls.config["BaseSettings"]:
            cls.app_base_settings[k.upper()] = cls.config["BaseSettings"][k.upper()]
        
        if os.environ['APP'] == "PROD":
            pass
        
        elif os.environ['APP'] == "DEV":

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
################################################################



################################################################
# FOR IOS DEBUGGING
################################################################
os.environ["OBJC_DISABLE_INITIALIZE_FORK_SAFETY"]="YES"
################################################################


# firebase_admin.initialize_app(options={'storageBucket': 'daisy-dsp.appspot.com'})
firebase_admin.initialize_app(options={'projectId':PROJECT})
DB = firestore.client()


