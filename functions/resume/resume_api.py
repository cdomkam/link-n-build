from firebase_functions import https_fn
from google.cloud import exceptions
import jsonschema
from jsonschema import validate
from typing import Any
import json

from resume.resume_db import set_resume, get_resume, create_resume
from constants import DB
from user.user_schema import create_user_schema, update_user_schema, get_user_sessions_schema, user_exist_schema
from user.user_db import get_user

create_resume_schema = {
    "type": "object",
    "properties": {
        "text":{"type":"string"}
    },
    "required": ["text"]
}

get_resume_schema = {
    "type": "object",
    "properties": {
        "user_id": {"type":"string"}
    },
    "required": ["user_id"]
}

@https_fn.on_call()
def createResume(req: https_fn.CallableRequest) -> Any:
    try:
        if not req.auth:
            message = 'You\'re unauthorized'
            raise exceptions.Unauthorized(message)
        
        validate(instance=req.data, schema=create_resume_schema)

        create_resume(req.data)
        return 
    
    except exceptions.Unauthorized:
        raise https_fn.HttpsError(code=https_fn.FunctionsErrorCode.UNAUTHENTICATED, message=message, details={"internalMessage": "You're unauthorized"})
    
    except jsonschema.exceptions.ValidationError as e:
        #TODO(cdomkam) might want to log e
        message = 'This is a bad request'
        raise https_fn.HttpsError(code=https_fn.FunctionsErrorCode.INVALID_ARGUMENT, message=message, details={"internalMessage": "Its a bad request"})

@https_fn.on_call()
def getResumesByUser(req: https_fn.CallableRequest) -> Any:
    try:
        if not req.auth:
            message = 'You\'re unauthorized'
            raise exceptions.Unauthorized(message)
        
        validate(instance=req.data, schema=get_resume_schema)

        user_id = req.auth.uid
        
        user_data = get_user(user_id=user_id)
        
        resume_ids = user_data["resume_ids"]
        resume_objs = []
        for id in resume_ids:
            resume_data = get_resume(resume_id=id)
            resume_objs.append(resume_data)
        
        # resume_data = get_resume(resume_id=resume_id)
        return {'data': resume_objs}
    
    except exceptions.Unauthorized:
        raise https_fn.HttpsError(code=https_fn.FunctionsErrorCode.UNAUTHENTICATED, message=message, details={"internalMessage": "You're unauthorized"})
    
    except jsonschema.exceptions.ValidationError as e:
        #TODO(cdomkam) might want to log e
        message = 'This is a bad request'
        raise https_fn.HttpsError(code=https_fn.FunctionsErrorCode.INVALID_ARGUMENT, message=message, details={"internalMessage": "Its a bad request"})

