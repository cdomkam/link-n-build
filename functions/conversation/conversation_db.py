from firebase_admin import firestore
from google.cloud.firestore_v1.base_query import FieldFilter
# from google.cloud.firestore import ArrayUnion, ArrayRemove
from typing import List, Any, Tuple, Dict
from database import (set_db_record, get_db_record, update_db_record)
from enum import Enum
# from functions.database import get_uid, get_timestamp
from constants import DB

class ConvDoc:
  def __init__(self) -> None:
    self.timestamp = firestore.SERVER_TIMESTAMP #; // when the account is created
    self.user_id: str
    self.comment: str= ""
    self.response: str= ""
    self.conversation_id: str=""
  
  @property
  def obj(self):
      return self.__dict__

def set_conv(data: dict) -> None:
    '''
    Set a User in a firestore db
    Args:

    Return:
    None
    '''

    conv_id = data['conversation_id']
    conv_data = ConvDoc().obj
    conv_data.update(data)
    set_db_record(db=DB, doc_id=conv_id, data=conv_data, collection_name="conversations")



def get_conv(conv_id: str) -> Any:
    '''
    Get a User from firestore db
    Args:

    Return:
    Dict
    '''
    conv_dict = get_db_record(db=DB, doc_id=conv_id, collection_name="conversations")
    return conv_dict


def update_conv(conv_id: str, conv_data: Dict):
    '''
    Update user in a firestore db
    Args:

    Return:
    None
    '''

    update_db_record(db=DB, doc_id=conv_id, data=conv_data, collection_name="conversations")

        
def delete_conv():
  '''
  Delete user in a firestore db
  Args:

  Return:
  None
  '''
  ...



def get_conversations_by(filter_by: str, filter_value: str, comparator: str)-> Any:
  '''Get user by a filter in the user doc
  Args:
    filter_by: The field to filter by in the doc
    filter_value: The value to filter by in the user doc
    comparator: can be ==, >=, <=, <, >
  Return:
    Query Snapshot
  '''

  conv_ref = DB.collection('users')
  conv_query = conv_ref.where(filter=FieldFilter(filter_by, comparator, filter_value))
  
  return conv_query.get()