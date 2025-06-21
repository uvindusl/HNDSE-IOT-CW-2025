import firebase_admin
from firebase_admin import credentials, firestore
import os
import time

SERVICE_ACCOUNT_KEY_PATH = os.environ.get('FIREBASE_SERVICE_ACCOUNT_KEY', 'Key.json')
COLLECTION_NAME = 'Accidents'

try :
    if not firebase_admin._apps:
        cred = credentials.Certificate(SERVICE_ACCOUNT_KEY_PATH)
        firebase_admin.initialize_app(cred)
    print("Fire Store Initialized")
except Exception as e:
    print(f"Error initializing Firebase Admin SDK: {e}")
    print("Please ensure 'SERVICE_ACCOUNT_KEY_PATH' is correct and the 'Key.json' file exists.")
    exit()

firestoreDb = firestore.client()

def detectChange(colSnapshot , changes , readTime):

    print(f"\nFirestore Collection Change Detected at {readTime}...")
    for change in changes:
        if change.type.name == 'ADDED':
            docData = change.document.to_dict()
            docId = change.document.id
            print(f"New document added: {docId}")

            if 'h_id' in docData:
                hIdValue = docData['h_id']
                print(f"  Extracted h_id: {hIdValue}")

            else:
                print(f"  Document {docId} does not contain an 'h_id' field.")
        elif change.type.name == 'MODIFIED':
            pass
        elif change.type.name == 'REMOVED':
            pass


print(f"Listening for new documents in collection: '{COLLECTION_NAME}'...")

colRef = firestoreDb.collection(COLLECTION_NAME)

queryWatch = colRef.on_snapshot(detectChange)

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print(f"\nListener stopped by user")

    queryWatch.unsubscribe()
    print('Firestore listener unsubscribed.')