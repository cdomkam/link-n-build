from firebase_admin import firestore
from google.cloud.firestore_v1.base_query import FieldFilter
from google.cloud.firestore import ArrayUnion, ArrayRemove
from typing import List, Any, Tuple, Dict
from database import (set_db_record, get_db_record, update_db_record)
from enum import Enum
from database import get_uid
from constants import DB



class ResumeDoc:
  def __init__(self) -> None:
    self.created_at = firestore.SERVER_TIMESTAMP #; // when the account is created
    self.resume_id: str
    self.text: str
  
  @property
  def obj(self):
      return self.__dict__


def create_resume(data: dict, resume_id: str | None=None) -> Tuple[dict, str]:
    ''' Creates a Conversation Object'''
    
    if resume_id is None: resume_id = get_uid()
    data.update({"resume_id":resume_id})
    resume_data = ResumeDoc().obj
    resume_data.update(data)
    return resume_data, resume_id

def set_resume(resume_id: str, resume_data: dict) -> None:
    '''
    Set a User in a firestore db
    Args:

    Return:
    None
    '''

    
    set_db_record(db=DB, doc_id=resume_id, data=resume_data, collection_name="resumes")



def get_resume(resume_id: str) -> Any:
    '''
    Get a User from firestore db
    Args:

    Return:
    Dict
    '''
    resume_dict = get_db_record(db=DB, doc_id=resume_id, collection_name="resumes")
    return resume_dict


def update_resume(resume_id: str, resume_data: Dict):
    '''
    Update user in a firestore db
    Args:

    Return:
    None
    '''

    update_db_record(db=DB, doc_id=resume_id, data=resume_data, collection_name="resumes")

        
def delete_resume():
  '''
  Delete user in a firestore db
  Args:

  Return:
  None
  '''
  ...



def get_resume_by(filter_by: str, filter_value: str, comparator: str)-> Any:
  '''Get user by a filter in the user doc
  Args:
    filter_by: The field to filter by in the doc
    filter_value: The value to filter by in the user doc
    comparator: can be ==, >=, <=, <, >
  Return:
    Query Snapshot
  '''

  resume_ref = DB.collection('resumes')
  resume_query = resume_ref.where(filter=FieldFilter(filter_by, comparator, filter_value))
  
  return resume_query.get()
