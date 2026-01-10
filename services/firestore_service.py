"""
Firestore Database Service
Handles all Firestore operations for users and documents
"""

from services.firebase_service import get_firestore_client
from datetime import datetime
from google.cloud.firestore_v1 import FieldFilter
from google.cloud import firestore

db = get_firestore_client()

# ==================== USER OPERATIONS ====================

def create_user(user_id, name, role="citizen", level=1):
    """
    Create a new user in Firestore
    
    Args:
        user_id: Unique user identifier
        name: User's full name
        role: "citizen" or "student"
        level: User level (default: 1)
    """
    user_ref = db.collection('users').document(user_id)
    user_ref.set({
        'name': name,
        'role': role,
        'level': level,
        'created_at': datetime.now()
    })
    return user_id

def get_user(user_id):
    """Get user by ID"""
    user_ref = db.collection('users').document(user_id)
    user = user_ref.get()
    if user.exists:
        return user.to_dict()
    return None

def update_user(user_id, **kwargs):
    """Update user fields"""
    user_ref = db.collection('users').document(user_id)
    user_ref.update(kwargs)

# ==================== DOCUMENT OPERATIONS ====================

def create_document(owner_id, title, summary, risk_flags, risk_score, file_url):
    """
    Create a new document in Firestore
    
    Args:
        owner_id: User ID who owns the document
        title: Document title
        summary: Document summary
        risk_flags: List of risk flags
        risk_score: Risk score (0-100)
        file_url: Cloud Storage URL
    
    Returns:
        Document ID
    """
    doc_ref = db.collection('documents').document()
    doc_ref.set({
        'ownerId': owner_id,
        'title': title,
        'summary': summary,
        'risk_flags': risk_flags,
        'risk_score': risk_score,
        'file_url': file_url,
        'uploaded_at': datetime.now()
    })
    return doc_ref.id

def get_document(doc_id):
    """Get document by ID"""
    doc_ref = db.collection('documents').document(doc_id)
    doc = doc_ref.get()
    if doc.exists:
        data = doc.to_dict()
        data['id'] = doc.id
        return data
    return None

def get_user_documents(owner_id, sort_by='newest', search_query=None, risk_filter=None):
    """
    Get all documents for a user with optional filtering and sorting
    
    Args:
        owner_id: User ID
        sort_by: 'newest', 'oldest', 'high_risk', 'low_risk'
        search_query: Search in title or summary
        risk_filter: 'high', 'medium', 'low'
    
    Returns:
        List of documents
    """
    # Simple query - just filter by owner (no composite index needed)
    query = db.collection('documents').where(filter=FieldFilter('ownerId', '==', owner_id))
    
    # Execute query
    docs = query.stream()
    
    # Convert to list and add IDs
    results = []
    for doc in docs:
        data = doc.to_dict()
        data['id'] = doc.id
        
        # Apply risk filter (client-side)
        if risk_filter:
            risk_score = data.get('risk_score', 0)
            if risk_filter == 'high' and risk_score < 70:
                continue
            elif risk_filter == 'medium' and (risk_score < 40 or risk_score >= 70):
                continue
            elif risk_filter == 'low' and risk_score >= 40:
                continue
        
        # Apply search filter (client-side)
        if search_query:
            search_lower = search_query.lower()
            if search_lower not in data.get('title', '').lower() and search_lower not in data.get('summary', '').lower():
                continue
        
        results.append(data)
    
    # Apply sorting (client-side)
    if sort_by == 'newest':
        results.sort(key=lambda x: x.get('uploaded_at', datetime.min), reverse=True)
    elif sort_by == 'oldest':
        results.sort(key=lambda x: x.get('uploaded_at', datetime.min))
    elif sort_by == 'high_risk':
        results.sort(key=lambda x: x.get('risk_score', 0), reverse=True)
    elif sort_by == 'low_risk':
        results.sort(key=lambda x: x.get('risk_score', 0))
    
    return results

def delete_document(doc_id):
    """Delete a document"""
    db.collection('documents').document(doc_id).delete()

def update_document(doc_id, **kwargs):
    """Update document fields"""
    doc_ref = db.collection('documents').document(doc_id)
    doc_ref.update(kwargs)
