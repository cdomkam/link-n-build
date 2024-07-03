import os
import firebase_admin
from firebase_admin import firestore

os.environ["OBJC_DISABLE_INITIALIZE_FORK_SAFETY"]="YES"

firebase_admin.initialize_app()
DB = firestore.client()
