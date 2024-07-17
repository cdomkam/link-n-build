from typing import Any

#TODO(cdomkam):
#check for unique usernames
# set a default drake photo
create_user_schema: dict[str,Any] = {
    "type": "object",
    "properties": {
        "username": {"type": "string"},
        "name": {"type": "string"},
    },
    "required": ["username","name"]
}

update_user_schema = {
    "type": "object",
    "properties": {
        "username": {"type": "string"},
        "name": {"type": "string"},
        "email": {"type": "string"},
        "image": {"type": "string"},
    }, # TODO: all fields are optional but one must be present
    "required": []
}

get_user_sessions_schema = {
    "type": "object",
    "properties": {
        "user_id": {"type": "string"},
    },
    "required": ["user_id"]
}


__all__ = ["create_user_schema", "update_user_schema", "get_user_sessions_schema"]