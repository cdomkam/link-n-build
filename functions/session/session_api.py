from firebase_functions import https_fn, options
from google.cloud import exceptions
import jsonschema
from jsonschema import validate
from typing import Any
from session.session_db import get_session
from constants import DB
from database import get_uid


get_session_schema = {
    "type": "object",
    "properties": {
        "session_id": {"type": "string"},
    },
    "required": ["session_id"]
}
@https_fn.on_call()
def getSession(req: https_fn.CallableRequest) -> https_fn.Response:
    '''Gets Entire Conversation from a user session with bot and returns it in markdown format'''
    
    try:
        if not req.auth:
            message = 'You\'re unauthorized'
            raise exceptions.Unauthorized(message)
        
        validate(instance=req.data, schema=get_session_schema)

        session_id = req.data.get('session_id')
        
        session = get_session(session_id=session_id)
        return {"data": session}
        
    except jsonschema.exceptions.ValidationError as e:
        message = 'This is a bad request'
        raise https_fn.HttpsError(code=https_fn.FunctionsErrorCode.INVALID_ARGUMENT, message=message, details={"internalMessage": "Its a bad request"})
    
    except:
        raise exceptions.InternalServerError("AHH Something Bad Happened!")