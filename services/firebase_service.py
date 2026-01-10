"""
Firebase Admin SDK Initialization Service
Initializes Firestore and Cloud Storage clients
"""

import firebase_admin
from firebase_admin import credentials, firestore, storage
import os

# Initialize Firebase Admin SDK
cred_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'firebase_admin.json')
cred = credentials.Certificate(cred_path)

try:
    firebase_admin.initialize_app(cred, {
        'storageBucket': f"{os.getenv('GCP_PROJECT_ID')}.appspot.com"
    })
    print("✅ Firebase Admin SDK initialized successfully")
except ValueError:
    # Already initialized
    print("ℹ️ Firebase Admin SDK already initialized")

# Get Firestore client
db = firestore.client()

# Get Cloud Storage bucket
bucket = storage.bucket()

def get_firestore_client():
    """Returns the Firestore client"""
    return db

def get_storage_bucket():
    """Returns the Cloud Storage bucket"""
    return bucket
