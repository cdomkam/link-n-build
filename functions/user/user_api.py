from firebase_functions import https_fn
from google.cloud import exceptions
import jsonschema
from jsonschema import validate
from typing import Any

from user.user_db import set_user, update_user
from constants import DB
from user.user_schema import create_user_schema, update_user_schema, create_settings_schema, save_track_schema, save_set_schema


@https_fn.on_call()
def createUser(req: https_fn.CallableRequest) -> Any:
    try:
        if not req.auth:
            message = 'You\'re unauthorized'
            raise exceptions.Unauthorized(message)
        
        validate(instance=req.data, schema=create_user_schema)
        
        user_id = req.auth.uid
        username = req.data["username"]
        name = req.data["name"]
        user_data = {"user_id":user_id, "username":username, "name":name}

        set_user( data=user_data)
        
        return 
    
    except exceptions.Unauthorized:
        raise https_fn.HttpsError(code=https_fn.FunctionsErrorCode.UNAUTHENTICATED, message=message, details={"internalMessage": "You're unauthorized"})
    
    except jsonschema.exceptions.ValidationError as e:
        #TODO(cdomkam) might want to log e
        message = 'This is a bad request'
        raise https_fn.HttpsError(code=https_fn.FunctionsErrorCode.INVALID_ARGUMENT, message=message, details={"internalMessage": "Its a bad request"})
    
@https_fn.on_call()
def updateUser(req: https_fn.CallableRequest) -> Any:
    try:
        if not req.auth:
            message = 'You\'re unauthorized'
            raise exceptions.Unauthorized(message)
        
        #image coming in as base64 encoded 
        validate(instance=req.data, schema=update_user_schema)

        user_id = req.auth.uid
        user_data = {}

        # Only add 'username' to user_data if it's present in the request
        if 'username' in req.data:
            user_data['username'] = req.data['username']

        # Only add 'image' to user_data if it's present in the request
        if 'image' in req.data:
            user_data['image'] = req.data['image']

        # Only add 'name' to user_data if it's present in the request
        if 'name' in req.data:
            user_data['name'] = req.data['name']

        # Update the user only if there is something to update
        if user_data:
            update_user(user_id=user_id, user_data=user_data)
        else:
            # Handle the case where no data is provided for update
            return {'message': 'No data provided for update'}

    except exceptions.Unauthorized:
        raise https_fn.HttpsError(code=https_fn.FunctionsErrorCode.UNAUTHENTICATED, message=message, details={"internalMessage": "You're unauthorized"})
    
    except jsonschema.exceptions.ValidationError as e:
        #TODO(cdomkam) might want to log e
        message = 'This is a bad request'
        raise https_fn.HttpsError(code=https_fn.FunctionsErrorCode.INVALID_ARGUMENT, message=message, details={"internalMessage": "Its a bad request"})
