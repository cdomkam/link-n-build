from firebase_admin import firestore
from google.cloud.firestore_v1.base_query import FieldFilter
from google.cloud.firestore import ArrayUnion, ArrayRemove
from typing import List, Any, Tuple, Dict
from database import (set_db_record, get_db_record, update_db_record)
from enum import Enum
from database import get_uid
from constants import DB



class SessionDoc:
  def __init__(self) -> None:
    self.created_at = firestore.SERVER_TIMESTAMP #; // when the account is created
    self.session_id: str=""
    self.user_id: str=""
    self.start: str=""
    self.end: str=""
    self.company_name: str=""
    self.role_name=""
    self.text: str=""
  
  @property
  def obj(self):
      return self.__dict__


def create_session(data: dict, session_id: str | None=None) -> Tuple[dict, str]:
    ''' Creates a Session Object'''
    
    if session_id is None: session_id = get_uid()
    data.update({"resume_id":session_id})
    session_data = SessionDoc().obj
    session_data.update(data)
    return session_data, session_id

def set_session(session_id: str, session_data: dict) -> None:
    '''
    Set a session in a firestore db
    Args:

    Return:
    None
    '''

    
    set_db_record(db=DB, doc_id=session_id, data=session_data, collection_name="sessions")



def get_session(session_id: str) -> Any:
    '''
    Get a session from firestore db
    Args:

    Return:
    Dict
    '''
    session_dict = get_db_record(db=DB, doc_id=session_id, collection_name="sessions")
    return session_dict


def update_session(session_id: str, session_data: Dict):
    '''
    Update session in a firestore db
    Args:

    Return:
    None
    '''

    update_db_record(db=DB, doc_id=session_id, data=session_data, collection_name="sessions")

        
def delete_session():
  '''
  Delete session in a firestore db
  Args:

  Return:
  None
  '''
  ...



def get_session_by(filter_by: str, filter_value: str, comparator: str)-> Any:
  '''Get session by a filter in the user doc
  Args:
    filter_by: The field to filter by in the doc
    filter_value: The value to filter by in the user doc
    comparator: can be ==, >=, <=, <, >
  Return:
    Query Snapshot
  '''

  session_ref = DB.collection('sessions')
  session_query = session_ref.where(filter=FieldFilter(filter_by, comparator, filter_value))
  
  return session_query.get()