import firebase_admin
from firebase_admin import credentials, firestore # Removed 'db' as it's not needed for Firestore
import os
import time

# It's good practice to get the key path from an environment variable for deployment,
# but ensure 'Key.json' is available locally for development if the env var isn't set.
SERVICE_ACCOUNT_KEY_PATH = os.environ.get('FIREBASE_SERVICE_ACCOUNT_KEY', 'Key.json')
COLLECTION_NAME = 'Accidents'

# Initialzing FireStore
try :
    if not firebase_admin._apps:
        cred = credentials.Certificate(SERVICE_ACCOUNT_KEY_PATH)
        firebase_admin.initialize_app(cred)
    print("Fire Store Initialized")
except Exception as e:
    print(f"Error initializing Firebase Admin SDK: {e}")
    print("Please ensure 'SERVICE_ACCOUNT_KEY_PATH' is correct and the 'Key.json' file exists.")
    exit()

# FireStore Database client instance
firestoreDb = firestore.client() # This is your correct Firestore client object

# Event Listener to detect new file is creat if creat get h_id
def detectChange(colSnapshot , changes , readTime):
    """
    Callback function that is invoked when there are changes in the watched collection.
    It identifies new documents and prints their 'h_id'.
    """
    print(f"\nFirestore Collection Change Detected at {readTime}...")
    for change in changes:
        if change.type.name == 'ADDED':
            docData = change.document.to_dict()
            docId = change.document.id
            print(f"New document added: {docId}")

            if 'h_id' in docData:
                hIdValue = docData['h_id']
                print(f"  Extracted h_id: {hIdValue}")
                # Add your further processing logic here if needed,
                # e.g., calling an API endpoint in your Flask app.
            else:
                print(f"  Document {docId} does not contain an 'h_id' field.")
        elif change.type.name == 'MODIFIED':
            # Add logic for modified documents if necessary
            pass
        elif change.type.name == 'REMOVED':
            # Add logic for removed documents if necessary
            pass


print(f"Listening for new documents in collection: '{COLLECTION_NAME}'...")

# Use firestoreDb (your Firestore client) to get the collection reference
colRef = firestoreDb.collection(COLLECTION_NAME)

# Set up the real-time listener using .on_snapshot()
queryWatch = colRef.on_snapshot(detectChange) # <-- Correct method is .on_snapshot()

try:
    while True:
        time.sleep(1) # Keep the script alive
except KeyboardInterrupt:
    print(f"\nListener stopped by user")
    # Unsubscribe the listener to clean up resources
    queryWatch.unsubscribe()
    print('Firestore listener unsubscribed.')