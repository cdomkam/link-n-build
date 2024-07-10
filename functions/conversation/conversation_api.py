from firebase_functions import https_fn, options
from google.cloud import exceptions
import jsonschema
from jsonschema import validate
from typing import Any
import json
from conversation.conversation_db import set_conv, create_conv
from user.user_db import get_user
from constants import DB
from database import get_uid

add_conv_schema: dict[str,Any] = {
    "type": "object",
    "properties": {
        "comment": {"type": "string"},
        "response": {"type": "string"},
        "user_id": {"type": "string"},
    },
    "required": ["comment", "response", "user_id"]
}

add_conv_batch_schema: dict[str,Any] = {
    "type": "object",
    "properties": {
        "comments": {"type": "array", "items":{"type":"string"}},
        "responses": {"type": "array", "items":{"type":"string"}},
        "user_id": {"type": "string"},
    },
    "required": ["comments", "responses", "user_id"]
}

# TODO:(cdomkam) FIGURE OUT HOW TO GET CORS TO WORK HERE
@https_fn.on_request(
    cors=options.CorsOptions(
        cors_origins=[r"firebase\.com$", r"https://flutter\.com"],
        cors_methods=["get"],
    )
)
def add_conversation(req: https_fn.Request) -> https_fn.Response:
    '''Adds a comment from an AI Model and a response from a Human user'''
    try:
        # print(req.data)
        # while True:
        #     chunk = req.data
        #     print(chunk)
        #     if chunk != b'':
        #         data = json.loads(req.data)
        #         break
        #     else:
        #         return {'data': None}
        
        # print(data)
        data = json.loads(req.data)
        validate(instance=data, schema=add_conv_schema)
        user_id = data.get('user_id')
        
        user_data = get_user(user_id=user_id) 
        username = user_data.get('username')
        name = user_data.get('name')
        
        data['username'] = username
        data['name'] = name
        

        conv_data,_ = create_conv(data=data)
        set_conv(conv_data=conv_data)
        
        return {"data": "SUCCESS"}
    
    except jsonschema.exceptions.ValidationError as e:
        message = 'This is a bad request'
        raise https_fn.HttpsError(code=https_fn.FunctionsErrorCode.INVALID_ARGUMENT, message=message, details={"internalMessage": "Its a bad request"})
    except:
        raise exceptions.InternalServerError("AHH Something Bad Happened!")

# TODO:(cdomkam) FIGURE OUT HOW TO GET CORS TO WORK HERE
@https_fn.on_request(
    cors=options.CorsOptions(
        cors_origins=[r"firebase\.com$", r"https://flutter\.com"],
        cors_methods=["get"],
    )
)
def add_conversation_batch(req: https_fn.Request) -> https_fn.Response:
    '''Adds comments and responses taken from a conversation and stores the result in firestore'''
    try:
        data = json.loads(req.data)
        
        validate(instance=data, schema=add_conv_batch_schema)

        user_id = data.get('user_id')
        comments = data.get('comments')
        responses = data.get('responses')

        user_data = get_user(user_id=user_id) 
        username = user_data.get('username')
        name = user_data.get('name')
        
        data['username'] = username
        data['name'] = name
        session_id = get_uid()
        for c, r in zip(comments, responses):
            conv_data = {
                "user_id": user_id,
                "name": name,
                "username":username,
                "comment":c,
                "response":r,
                "session_id":session_id
            }
            
            conv_data, _ = create_conv(data=conv_data)
            set_conv(conv_data=conv_data)
        return {"data": "SUCCESS"}
        
    except jsonschema.exceptions.ValidationError as e:
        message = 'This is a bad request'
        raise https_fn.HttpsError(code=https_fn.FunctionsErrorCode.INVALID_ARGUMENT, message=message, details={"internalMessage": "Its a bad request"})
    
    except:
        raise exceptions.InternalServerError("AHH Something Bad Happened!")    