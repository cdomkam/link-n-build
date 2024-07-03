import uuid
from google.cloud.firestore_v1.base_query import FieldFilter
from firebase_admin import firestore, storage
from typing import List, Any, Tuple, Dict, Callable
# import firebase_admin
# from firebase_admin import credentials

def get_uid() -> str:
    new_uuid = uuid.uuid4()
    id = str(new_uuid)
    return id

def get_timestamp():
    return firestore.firestore.SERVER_TIMESTAMP



def set_db_record(db: firestore.client, 
                  data: dict, doc_id: str | Any | None, 
                  collection_name: str = "DEV") -> None:
    '''Sets a record in firestore'''
    
    ref = db.collection(collection_name).document(doc_id)
    ref.set(data)

def get_db_record(db: firestore.client, 
                  doc_id: str | Any | None, 
                  collection_name: str = "DEV") -> Any:
    '''Gets a database record from firestore'''
    ref = db.collection(collection_name).document(doc_id)
    doc = ref.get()
    return doc.to_dict()

def update_db_record(db: firestore.client, 
                     doc_id: str | Any | None, 
                     data: Dict, 
                     collection_name: str = "DEV"):
    '''Updates a DB record in firestore'''
    ref = db.collection(collection_name).document(doc_id)
    dict = ref.get().to_dict()

    if dict is not None:
        dict_keys = dict.keys()
        for k, v in data.items():
            if k in dict_keys:
                dict[k] = v
        
        ref.update(dict)

def set_subcollection(db: firestore.client, 
                      doc_id: str | Any | None, 
                      collection_name: str, 
                      subcollection_name: str) -> None:
    '''Sets a subcollection'''

    collection_ref = db.collection(collection_name).document(doc_id)
    collection_ref.collection(subcollection_name)

def set_doc_in_subcollection(db: firestore.client, 
                             collection_doc_id: str,
                             subcollection_doc_id: str, 
                             doc_data: dict, 
                             collection_name: str, 
                             subcollection_name: str,) -> None:
    '''Creates a subcollection with a document inside'''
    # if subcollection_doc_id is None: 
    #     subcollection_doc_id = get_uid()

    collection_ref = db.collection(collection_name).document(collection_doc_id)
    
        
    # subcollection_doc_id = get_uid()
    collection_subcollection_ref = collection_ref.collection(subcollection_name).document(subcollection_doc_id)
    collection_subcollection_ref.set(doc_data)

def get_doc_in_subcollection(db: firestore.client, 
                             collection_doc_id: str | Any,
                             subcollection_doc_id: str | Any,
                             collection_name: str, 
                             subcollection_name: str) -> Any:
    '''Gets a document with a subcollection inside'''

    collection_ref = db.collection(collection_name).document(collection_doc_id)
     
    subcollection_doc_id = get_uid()
    collection_subcollection_ref = collection_ref.collection(subcollection_name).document(subcollection_doc_id)
    
    return collection_subcollection_ref.get().to_dict()

def update_doc_in_subcollection(db: firestore.client, 
                             collection_doc_id: str | Any,
                             subcollection_doc_id: str | Any,
                             subcollection_data: dict,
                             collection_name: str, 
                             subcollection_name: str) -> Any:
    '''Updates a Doc in a subcollection'''
    collection_ref = db.collection(collection_name).document(collection_doc_id)
    collection_subcollection_ref = collection_ref.collection(subcollection_name).document(subcollection_doc_id)

    subcollection_dict = collection_subcollection_ref.get().to_dict()
    if subcollection_dict is not None:
        subcollection_keys = subcollection_dict.keys()
        for key, value in subcollection_data.items():
            if key in subcollection_keys:
                subcollection_dict[key] = value
        collection_subcollection_ref.update(subcollection_dict)

def download_file_from_url(url: str, file_name: str) -> str:
    import requests

    with open(file_name, "wb") as f:
            f.write(requests.get(url).content)
    return f"{file_name}"

def set_blob_metadata(blob: Any):
    """Set a blob's metadata."""
    raise NotImplemented
    # bucket_name = 'your-bucket-name'
    # blob_name = 'your-object-name'

    # storage_client = storage.Client()
    # bucket = storage_client.bucket(bucket_name)
    # blob = bucket.get_blob(blob_name)
    metageneration_match_precondition = None

    # Optional: set a metageneration-match precondition to avoid potential race
    # conditions and data corruptions. The request to patch is aborted if the
    # object's metageneration does not match your precondition.
    metageneration_match_precondition = blob.metageneration
    # print(dir(blob))
    # metadata = {'cache-control':'no-store, max-age=86400'}

    # blob.metadata = metadata
    blob.cache_control = 'no-store, max-age=86400'
    blob.patch(if_metageneration_match=metageneration_match_precondition)

    # print(f"The metadata for the blob {blob.name} is {blob.metadata}")

def upload_file_to_storage(local_file_path: str, cloud_file_path: str, bucket_name: None=None, set_meta_data: Callable|None=None) -> None:
    '''
    Adds a file in filesystem to storage
    '''
    raise NotImplemented
    
    bucket = storage.bucket(name=bucket_name)
    blob = bucket.blob(cloud_file_path)
    
    blob.upload_from_filename(local_file_path)

    if set_meta_data is not None:
        set_meta_data(blob=blob)
    # print('Data added to firebase Storage!')

def download_file_from_storage(file_name: str, bucket_name: None=None) -> str:
    '''
    Download a file from storage to the tmp folder
    '''
    raise NotImplemented

    bucket = storage.bucket(name=bucket_name)
    blob = bucket.blob(file_name)
    name=file_name.split("/")[-1]

    with open(f"/tmp/{name}", 'wb') as file_obj:
        blob.download_to_file(file_obj=file_obj)
    
    return f"/tmp/{name}"


def download_b64_image_from_storage(file_name: str) -> None:
    ''' Downloads base64 encoded string from firebae storage'''
    raise NotImplemented

    import io
    from PIL import Image
    import base64

    bucket = storage.bucket()
    blob = bucket.blob(file_name)
    base64_data_downloaded = blob.download_as_string()
    image_data_decoded = base64.b64decode(base64_data_downloaded)
    
    with open('downloaded_image.jpg', 'wb') as image_file:
        image_file.write(image_data_decoded)

    print("Base64-encoded image downloaded and saved.")

def download_audio_from_storage(file_name: str) -> None:
    ''' Downloads base64 encoded string from firebae storage'''
    raise NotImplemented

    bucket = storage.bucket()
    blob = bucket.blob(file_name)
    base64_data_downloaded = blob.download_as_file()

