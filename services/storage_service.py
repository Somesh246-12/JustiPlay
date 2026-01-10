"""
Cloud Storage Service
Handles file uploads to Google Cloud Storage
"""

from services.firebase_service import get_storage_bucket
from datetime import datetime, timedelta
import os

bucket = get_storage_bucket()

def upload_document(file, user_id, filename=None):
    """
    Upload a document to Cloud Storage
    
    Args:
        file: File object from Flask request
        user_id: User ID for organizing files
        filename: Optional custom filename
    
    Returns:
        dict with file_url and blob_name
    """
    # Generate unique filename
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    if filename:
        # Sanitize filename
        safe_filename = "".join(c for c in filename if c.isalnum() or c in (' ', '.', '_')).rstrip()
        file_extension = os.path.splitext(safe_filename)[1]
        blob_name = f"documents/{user_id}/{timestamp}_{safe_filename}"
    else:
        blob_name = f"documents/{user_id}/{timestamp}.pdf"
    
    # Upload to Cloud Storage
    blob = bucket.blob(blob_name)
    blob.upload_from_file(file, content_type='application/pdf')
    
    # Make the blob publicly accessible (optional, for demo purposes)
    # For production, use signed URLs instead
    blob.make_public()
    
    return {
        'file_url': blob.public_url,
        'blob_name': blob_name,
        'gs_url': f"gs://{bucket.name}/{blob_name}"
    }

def get_signed_url(blob_name, expiration_minutes=60):
    """
    Generate a signed URL for private file access
    
    Args:
        blob_name: Path to file in storage
        expiration_minutes: URL validity duration
    
    Returns:
        Signed URL string
    """
    blob = bucket.blob(blob_name)
    url = blob.generate_signed_url(
        version="v4",
        expiration=timedelta(minutes=expiration_minutes),
        method="GET"
    )
    return url

def delete_file(blob_name):
    """Delete a file from Cloud Storage"""
    blob = bucket.blob(blob_name)
    blob.delete()

def file_exists(blob_name):
    """Check if a file exists in Cloud Storage"""
    blob = bucket.blob(blob_name)
    return blob.exists()
