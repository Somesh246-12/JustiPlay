# Firebase Storage Setup Guide

## Current Status
✅ **Firestore** - Working (documents being saved)  
⚠️ **Cloud Storage** - Bucket doesn't exist yet

## Quick Fix: Create Storage Bucket

### Option 1: Firebase Console (Recommended - 2 minutes)

1. **Go to Firebase Storage Console**:
   https://console.firebase.google.com/project/legalease-ai-471416/storage

2. **Click "Get Started"**

3. **Choose Security Rules**:
   - For hackathon/demo: Select **"Start in test mode"**
   - This allows read/write for 30 days
   - Click **"Next"**

4. **Choose Location**:
   - Select **"us-central"** (or closest to you)
   - Click **"Done"**

5. **Wait 30 seconds** for bucket creation

### Option 2: Google Cloud Console

1. Go to: https://console.cloud.google.com/storage/browser?project=legalease-ai-471416

2. Click **"CREATE BUCKET"**

3. Configure:
   - Name: `legalease-ai-471416.appspot.com`
   - Location: **us-central1**
   - Storage class: **Standard**
   - Access control: **Uniform**

4. Click **"CREATE"**

### Option 3: gcloud CLI

```bash
# Create bucket
gsutil mb -p legalease-ai-471416 -c STANDARD -l us-central1 gs://legalease-ai-471416.appspot.com

# Make bucket public (for demo)
gsutil iam ch allUsers:objectViewer gs://legalease-ai-471416.appspot.com
```

## After Creating Bucket

### 1. Restart Flask Server
```bash
# Stop current server (Ctrl+C)
python app.py
```

### 2. Test Upload
- Go to Document Analysis
- Upload a PDF
- Check terminal for:
  ```
  ✅ File uploaded to Cloud Storage
  ✅ Document saved to Firestore: [doc-id]
  ```

### 3. Verify in Console
- **Storage**: https://console.firebase.google.com/project/legalease-ai-471416/storage
  - Should see: `documents/default_user/[timestamp]_filename.pdf`

- **Firestore**: https://console.firebase.google.com/project/legalease-ai-471416/firestore
  - Should see: `documents` collection with your uploaded files

## Current Workaround (Already Implemented)

The code now works **without Cloud Storage**:
- ✅ Documents save to Firestore
- ✅ Library displays documents
- ✅ Download uses local PDF files
- ⚠️ Files stored in `tmp_docs/` instead of cloud

This means you can **demo the library feature NOW** even without setting up storage!

## What's Working Right Now

### ✅ Without Storage Bucket
- Document analysis ✅
- Firestore save ✅
- Document library ✅
- Search/filter/sort ✅
- View document details ✅
- Download PDF (local) ✅

### ✅ With Storage Bucket (After Setup)
- All above features ✅
- Cloud-hosted PDFs ✅
- Persistent file storage ✅
- Shareable download links ✅

## Testing the Library

1. **Upload a document**:
   - Go to `/document/upload`
   - Upload any PDF
   - Wait for analysis

2. **Check Firestore**:
   - Terminal should show: `✅ Document saved to Firestore: [id]`
   - No more index errors!

3. **View Library**:
   - Go to `/citizen/library`
   - Should see your uploaded document
   - Try search, filter, sort

4. **View Details**:
   - Click "View Analysis"
   - See full document details
   - Download PDF works (local file)

## Security Rules (For Production)

Once bucket is created, update rules in Firebase Console:

```javascript
rules_version = '2';
service firebase.storage {
  match /b/{bucket}/o {
    match /documents/{userId}/{fileName} {
      // Only owner can read/write their documents
      allow read, write: if request.auth != null && request.auth.uid == userId;
    }
  }
}
```

For hackathon demo, test mode is fine!

## Summary

**Current State**:
- ✅ Firestore queries fixed (no index needed)
- ✅ Documents save even without storage
- ✅ Library works with local files
- ⚠️ Storage bucket needs creation (optional for demo)

**Next Step**:
- Create storage bucket (2 minutes)
- OR continue using local files for demo
