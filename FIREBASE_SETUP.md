# Firebase Document Library - Implementation Guide

## Overview
This implementation adds Firebase/Firestore integration for persistent document storage and a searchable document library for citizens.

## Architecture

### Services Created

1. **`services/firebase_service.py`**
   - Initializes Firebase Admin SDK
   - Provides Firestore and Cloud Storage clients
   - Auto-initializes on import

2. **`services/firestore_service.py`**
   - User CRUD operations
   - Document CRUD operations
   - Advanced querying with filters and sorting
   - Client-side search functionality

3. **`services/storage_service.py`**
   - Upload PDFs to Cloud Storage
   - Generate public/signed URLs
   - File management utilities

### Firestore Schema

```
users/
  {userId}/
    - name: string
    - role: "citizen" | "student"
    - level: number (default: 1)
    - created_at: timestamp

documents/
  {docId}/
    - ownerId: string (references users)
    - title: string
    - summary: string (max 500 chars)
    - risk_flags: array (max 5 high-risk clauses)
    - risk_score: number (0-100)
    - file_url: string (Cloud Storage URL)
    - uploaded_at: timestamp
```

### Cloud Storage Structure

```
gs://{project-id}.appspot.com/
  documents/
    {userId}/
      {timestamp}_{filename}.pdf
```

## Features Implemented

### 1. Document Upload with Firebase
- **Route**: `/document/analyze` (POST)
- **Flow**:
  1. User uploads PDF
  2. Document AI extracts text
  3. Gemini analyzes risk
  4. File uploaded to Cloud Storage
  5. Metadata saved to Firestore
  6. Analysis displayed to user

### 2. Document Library
- **Route**: `/citizen/library`
- **Features**:
  - Search by title/keywords
  - Sort by: Newest, Oldest, High Risk, Low Risk
  - Filter by risk level: High, Medium, Low
  - Responsive card layout
  - Empty state for new users

### 3. View Document Analysis
- **Route**: `/citizen/document/<doc_id>`
- **Features**:
  - Full document details
  - Risk score visualization
  - Risk flags display
  - Personalized recommendations
  - Download original PDF
  - Back to library navigation

## User Flow

```
1. Citizen Dashboard
   ↓
2. Click "Document Analysis" or "Document Library"
   ↓
3a. Upload New Document          3b. Browse Library
    → Document AI Processing         → Search/Filter/Sort
    → Gemini Risk Analysis           → View Document
    → Save to Firebase               → See Full Analysis
    → View Results                   → Download PDF
    ↓                                ↓
4. Document saved to library     4. Return to library or upload new
```

## Configuration

### Environment Variables
Ensure these are set in `.env`:
```
GCP_PROJECT_ID=your-project-id
GEMINI_API_KEY=your-api-key
```

### Firebase Service Account
Place `firebase_admin.json` in `config/` directory with:
- Service account credentials
- Storage bucket access
- Firestore permissions

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Verify Firebase credentials:
```bash
# Check config/firebase_admin.json exists
ls config/firebase_admin.json
```

3. Run the application:
```bash
python app.py
```

## Testing the Integration

### Test Document Upload
1. Login as citizen
2. Go to "Document Analysis"
3. Upload a PDF
4. Verify:
   - Analysis completes
   - File appears in Cloud Storage console
   - Document appears in Firestore console
   - Document appears in library

### Test Library Features
1. Go to "Document Library"
2. Test search: Enter keywords
3. Test sorting: Try all sort options
4. Test filtering: Filter by risk level
5. Click "View Analysis" on a document
6. Verify all data displays correctly

## Troubleshooting

### Firebase Not Initializing
- Check `config/firebase_admin.json` exists
- Verify service account has correct permissions
- Check console for initialization errors

### Documents Not Saving
- Verify Firestore database is created
- Check IAM permissions for service account
- Look for errors in terminal output

### Files Not Uploading
- Verify Storage bucket exists
- Check bucket name in `firebase_service.py`
- Ensure service account has Storage Admin role

### Search Not Working
- Search is client-side (Firestore limitation)
- Large result sets may be slow
- Consider implementing Algolia for production

## Future Enhancements

1. **Full-text Search**: Integrate Algolia or Elasticsearch
2. **Pagination**: Add pagination for large libraries
3. **Batch Operations**: Delete/export multiple documents
4. **Sharing**: Share documents with students/experts
5. **Analytics**: Track document trends and patterns
6. **Notifications**: Alert on high-risk documents
7. **Export**: Download library as CSV/Excel

## Security Notes

- Files are currently public (for demo)
- Production should use signed URLs
- Add user authentication checks
- Implement rate limiting
- Validate file types and sizes
- Sanitize user inputs

## Performance Considerations

- Firestore queries are indexed automatically
- Composite indexes may be needed for complex queries
- Cloud Storage has generous free tier
- Consider CDN for file delivery at scale
- Implement caching for frequently accessed documents
