
import os
from firebase_functions import https_fn
from google.cloud import exceptions
import jsonschema
from jsonschema import validate
# from constants import *
from typing import Dict

from user.user_api import *


hello_LNB_schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
    },
    "required": ["name"]
}


@https_fn.on_call()
def hello_lnb(req: https_fn.CallableRequest) -> Dict[str,str]:
    try:
        # print(data)
        # Checking if the request is made by an authenticated user
        if not req.auth:
            message = 'You\'re unauthorized'
            raise exceptions.Unauthorized(message)

        validate(instance=req.data, schema=hello_LNB_schema)
        
        # Accessing the parameters sent in the request
        name = req.data['name']

        # Performing some action, for example, returning a greeting
        greeting = f'Hello, {name}!'


        # Returning a response to the client
        return {'message': greeting}

    # Handling errors and returning them to the client
    except exceptions.Unauthorized:
        raise https_fn.HttpsError(code=https_fn.FunctionsErrorCode.UNAUTHENTICATED, message=message, details={"internalMessage": "You're unauthorized"})
    
    except jsonschema.exceptions.ValidationError as e:
        #TODO(cdomkam) might want to log e
        message = 'This is a bad request'
        raise https_fn.HttpsError(code=https_fn.FunctionsErrorCode.INVALID_ARGUMENT, message=message, details={"internalMessage": "Its a bad request"})





   