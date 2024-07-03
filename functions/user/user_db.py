from firebase_admin import firestore
from google.cloud.firestore_v1.base_query import FieldFilter
from google.cloud.firestore import ArrayUnion, ArrayRemove
from typing import List, Any, Tuple, Dict
from functions.database import (set_db_record, get_db_record, update_db_record)
from enum import Enum
# from functions.database import get_uid, get_timestamp
from constants import DB



class UserDoc:
  def __init__(self) -> None:
    self.timestamp = firestore.SERVER_TIMESTAMP #; // when the account is created
    self.user_id: str
    self.name: str = ""#string; // name
    self.username: str= "" #string; // username
    self.comment: str= ""
    self.response: str= ""
  
  @property
  def obj(self):
      return self.__dict__

def set_user(data: dict) -> None:
    '''
    Set a User in a firestore db
    Args:

    Return:
    None
    '''

    user_id = data['user_id']
    user_data = UserDoc().obj
    user_data.update(data)
    set_db_record(db=DB, doc_id=user_id, data=user_data, collection_name="users")



def get_user(user_id: str) -> Any:
    '''
    Get a User from firestore db
    Args:

    Return:
    Dict
    '''
    user_dict = get_db_record(db=DB, doc_id=user_id, collection_name="users")
    return user_dict


def update_user(user_id: str, user_data: Dict):
    '''
    Update user in a firestore db
    Args:

    Return:
    None
    '''

    update_db_record(db=DB, doc_id=user_id, data=user_data, collection_name="users")

        
def delete_user():
  '''
  Delete user in a firestore db
  Args:

  Return:
  None
  '''
  ...



def get_users_by(filter_by: str, filter_value: str, comparator: str)-> Any:
  '''Get user by a filter in the user doc
  Args:
    filter_by: The field to filter by in the doc
    filter_value: The value to filter by in the user doc
    comparator: can be ==, >=, <=, <, >
  Return:
    Query Snapshot
  '''

  user_ref = DB.collection('users')
  user_query = user_ref.where(filter=FieldFilter(filter_by, comparator, filter_value))
  
  return user_query.get()
