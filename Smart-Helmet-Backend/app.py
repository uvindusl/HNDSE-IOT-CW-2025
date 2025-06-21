from flask import Flask, jsonify
from flask_cors import CORS
import threading
import time
import os
import firebase_admin
from firebase_admin import credentials, firestore , db


app = Flask(__name__)
CORS(app)
# Configuration for firebase
SERVICE_ACCOUNT_KEY_PATH = os.environ.get('FIREBASE_SERVICE_ACCOUNT_KEY', 'Key.json')
REALTIME_DATABASE_URL = os.environ.get('FIREBASE_RTDB_URL', 'https://smarthelmet-3a072-default-rtdb.firebaseio.com/')
RTDB_LISTEN_PATH = os.environ.get('FIREBASE_RTDB_LISTEN_PATH', '/')
COLLECTION_NAME = 'Accidents'

# Initialize Firebase Admin SDK
if not firebase_admin._apps:
    try:
        cred = credentials.Certificate(SERVICE_ACCOUNT_KEY_PATH)
        firebase_admin.initialize_app(cred , {
            'databaseURL': REALTIME_DATABASE_URL
        })
        print('Firebase Admin SDK initialized.')
    except Exception as e:
        print(f"Error initializing Firebase Admin SDK: {e}")

# Real time Database
realTimeDbRef = db.reference(RTDB_LISTEN_PATH)

# FireStore Database
firestoreDb = firestore.client()

#this will be change in future it will come to backend from mobile app or firebase idk
helmetID =  "h0222"

@app.route('/riders', methods=['GET'])
def getRiderDetails():
    riderData = firestoreDb.collection('Riders').where('h_id', '==', helmetID)
    docs = riderData.get()

    riderData = []
    for doc in docs:
        riderData.append(doc.to_dict())
    return jsonify(riderData)

@app.route('/accidents', methods=['GET'])
def getAccidentDetails():
    accidentData = firestoreDb.collection('Accidents').where('h_id', '==', helmetID)
    docs = accidentData.get()

    accidentData = []
    for doc in docs:
        accidentData.append(doc.to_dict())
    return jsonify(accidentData)

@app.route('/vitals' , methods=['GET'])
def getVitalDetails():
    vitalData = firestoreDb.collection('Vitals').where('h_id', '==', helmetID)
    docs = vitalData.get()

    vitalData = []
    for doc in docs:
        vitalData.append(doc.to_dict())
    return jsonify(vitalData)


def realTimeDBListner(event):
    print(f"\n[RTDB Listener] Event Received: {event.event_type} at {event.path}")

    try:
        pathParts = [part for part in event.path.strip('/').split('/') if part]

        if len(pathParts) == 2 and pathParts[1] == 'heart_beat':
            documentId = pathParts[0]
            heartBeatValue = event.data

            firestoreCollectionName = 'Vitals'
            docRef = firestoreDb.collection(firestoreCollectionName).document(documentId)

            if event.event_type == 'put' or event.event_type == 'patch':
                if heartBeatValue is not None:
                    newRecord = heartBeatValue

                    doc = docRef.get()

                    if doc.exists:
                        docData = doc.to_dict()
                        currentReadings = docData.get('heartbeat_readings', [])
                        currentReadings.append(newRecord)
                        docRef.update({'heartbeat_readings': currentReadings})

                        print(
                            f"[RTDB Listener] Appended new heartbeat to '{documentId}' in '{firestoreCollectionName}'.")
                    else:
                        docRef.set({
                            'heartbeat_readings': [newRecord],
                            'h_id': documentId,
                        })
                        print(f"[RTDB Listener] Created new document '{documentId}' in '{firestoreCollectionName}'.")
                else:
                    print(f"[RTDB Listener] heartbeat child for '{documentId}' was set to None (deleted).")
            else:
                print(f"[RTDB Listener] Unhandled event type for heart_beat: {event.event_type}")

        else:
            print(
                f"[RTDB Listener] Path '{event.path}' does not match expected '/{{hxxx}}/heart_beat' pattern. Skipping")
    except Exception as e:
        print(f"[RTDB Listener] Error processing Realtime Database event: {e}")


def startRealTimeDbLisner():
    print(f"[RTDB Listener] Starting Listener for path: {RTDB_LISTEN_PATH}...")

    try:
        realTimeDbRef.listen(realTimeDBListner)
        print("[RTDB Listener] Listener started successfully.")
    except Exception as e:
        print(f"[RTDB Listener] Listener terminated with error: {e}")
    print("[RTDB Listener] Listener stopped unexpectedly.")

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



if __name__ == '__main__':
    print("Starting Smart Helmet Backend Server...")

    # Set default environment variables for direct run
    os.environ.setdefault('FIREBASE_RTDB_URL', 'https://smarthelmet-3a072-default-rtdb.firebaseio.com/')
    os.environ.setdefault('FIREBASE_RTDB_LISTEN_PATH', '/')

    # Start the Firebase listener in a daemon thread
    listener_thread = threading.Thread(target=startRealTimeDbLisner, daemon=True)
    listener_thread.start()
    print("[RTDB Listener] Daemon thread for listener started.")

    print(f"Listening for new documents in collection: '{COLLECTION_NAME}'...")

    colRef = firestoreDb.collection(COLLECTION_NAME)

    queryWatch = colRef.on_snapshot(detectChange)

    # Start Flask app (this will block the main thread)
    print("Starting Flask application on port 5000...")
    try:
        app.run(debug=False, port=5000)
    except KeyboardInterrupt:
        print("\nServer stopped by user.")
    except Exception as e:
        print(f"Flask app error: {e}")

    print("Application shutdown complete.")
