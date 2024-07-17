from firebase_admin import firestore
from google.cloud.firestore_v1.base_query import FieldFilter
# from google.cloud.firestore import ArrayUnion, ArrayRemove
from typing import List, Any, Tuple, Dict
from database import (set_db_record, get_db_record, update_db_record)
from enum import Enum
from database import get_uid, get_timestamp
from constants import DB

class ConvDoc:
  def __init__(self) -> None:
    self.timestamp = firestore.SERVER_TIMESTAMP #; // when the account is created
    self.user_id: str
    self.comment: str= ""
    self.response: str= ""
    self.conv_id: str=""
    self.session_id: str=""
  
  @property
  def obj(self):
      return self.__dict__

def create_conv(data: dict, conv_id: str | None=None) -> Tuple[dict, str]:
    ''' Creates a Conversation Object'''
    
    if conv_id is None: conv_id = get_uid()
    data.update({"conv_id":conv_id})
    conv_data = ConvDoc().obj
    conv_data.update(data)
    return conv_data, conv_id

def set_conv(conv_data: dict) -> None:
    '''
    Set a User in a firestore db
    Args:

    Return:
    None
    '''

    conv_id = conv_data['conv_id']
    set_db_record(db=DB, doc_id=conv_id, data=conv_data, collection_name="conversations")



def get_conv(conv_id: str) -> Any:
    '''
    Get a Conversation from firestore db
    Args:

    Return:
    Dict
    '''
    conv_dict = get_db_record(db=DB, doc_id=conv_id, collection_name="conversations")
    return conv_dict


def update_conv(conv_id: str, conv_data: Dict):
    '''
    Update Conversation in a firestore db
    Args:

    Return:
    None
    '''

    update_db_record(db=DB, doc_id=conv_id, data=conv_data, collection_name="conversations")

        
def delete_conv():
  '''
  Delete Conversation in a firestore db
  Args:

  Return:
  None
  '''
  ...



def get_conversations_by(filter_by: str, filter_value: str, comparator: str)-> Any:
  '''Get Converation by a filter in the user doc
  Args:
    filter_by: The field to filter by in the doc
    filter_value: The value to filter by in the user doc
    comparator: can be ==, >=, <=, <, >
  Return:
    Query Snapshot
  '''

  conv_ref = DB.collection('conversations')
  conv_query = conv_ref.where(filter=FieldFilter(filter_by, comparator, filter_value))
  
  return conv_query.get()

def get_conversation_from_session(name: str, session_id:str) -> str:
  
  conv_docs = get_conversations_by(filter_by="session_id", filter_value=session_id, comparator="==")
  
  
  chunk=f"<h1>Conversation with {name}</h1>"
  for conv_doc in conv_docs:
    conv_dict = conv_doc.to_dict()
    comment = conv_dict['comment']
    response = conv_dict['response']
    
    chunk += f"<b>Question</b>: {comment}<br><b>Answer</b>: {response}<br><br>"
  
  return chunk