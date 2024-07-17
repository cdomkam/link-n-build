from firebase_functions import https_fn
from google.cloud import exceptions
import jsonschema
from jsonschema import validate
from typing import Any
import json

from user.user_db import set_user, update_user, get_user
from constants import DB
from user.user_schema import create_user_schema, update_user_schema, get_user_sessions_schema


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

@https_fn.on_request()
def getUserSessions(req: https_fn.CallableRequest) -> Any:
    try:
        data = json.loads(req.data)
        
        validate(instance=data, schema=get_user_sessions_schema)
        user_id = data.get('user_id')
        user_dict = get_user(user_id=user_id)
        session_ids = user_dict['session_ids']
        
        return {"data": session_ids}
    
    except jsonschema.exceptions.ValidationError as e:
        message = 'This is a bad request'
        raise https_fn.HttpsError(code=https_fn.FunctionsErrorCode.INVALID_ARGUMENT, message=message, details={"internalMessage": "Its a bad request"})
    
    except:
        raise exceptions.InternalServerError("AHH Something Bad Happened!") 