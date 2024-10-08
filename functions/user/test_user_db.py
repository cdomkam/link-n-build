import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + "/../")

from user_db import set_user
from database import get_uid
from constants import make_a_request, BASE_FUNCTION_URL

def test_create_user():
    # from constants import DB
    user_id="user123"
    data={
        "user_id":user_id,
        "name":"my_name",
        "username":"my_username"
    }
    set_user(data=data)
    ... 

def create_user_data(data: dict):
    
    
    set_user(data=data)
    ...

def test_get_user_sessions():
    # from constants import make_a_request, BASE_FUNCTION_URL
    
    function_url = BASE_FUNCTION_URL + "getUserSessions"
    print(function_url)
    data = {"user_id":"c1dbf4a1-b2af-4423-9c07-2d9a98806ff5"}
    
    make_a_request(function_url=function_url, data=data)
    ...

def test_user_exists():
    function_url = BASE_FUNCTION_URL + "userExist"
    data = {"user_id":"c66efcb7-1e0a-4d30-a867-cda28e06a845"}
    
    result = make_a_request(function_url=function_url, data=data)
    print(result['data'])

if __name__=="__main__":
    
    data={
        
        "user_id":get_uid(),
        "name":"Alex Durazo",
        "username":"aDurazo"
    }

    create_user_data(data=data)
    # test_get_user_sessions()
    # test_user_exists()