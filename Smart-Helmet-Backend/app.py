from flask import Flask, jsonify , request , redirect , url_for
from flask_cors import CORS
import threading
import time
import os
import firebase_admin
from firebase_admin import credentials, firestore , db
import uuid
from datetime import datetime , timedelta
import requests

app = Flask(__name__)

# This is for connect backend with frontend
CORS(app)

# Configuration for firebase
SERVICE_ACCOUNT_KEY_PATH = os.environ.get('FIREBASE_SERVICE_ACCOUNT_KEY', 'Key.json')
REALTIME_DATABASE_URL = os.environ.get('FIREBASE_RTDB_URL', 'https://smarthelmet-3a072-default-rtdb.firebaseio.com/')
RTDB_LISTEN_PATH = os.environ.get('FIREBASE_RTDB_LISTEN_PATH', '/')
COLLECTION_NAME = 'Accidents'

initial_load_complete = False

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

# varible to store h_id coming from detectchange function
helmetID =  None

app.config['SERVER_NAME'] = 'localhost:5000'
REACT_FRONTEND_BASE_URL = "http://localhost:5173"

unique_dashboard_access_tokens = {}

USER_ID = "29722"
API_KEY = "FmoNwwAeeuDzuLfgmXPv"

TO_NUMBER = "94702004065"
SENDER_ID = "NotifyDEMO"

url = "https://app.notify.lk/api/v1/send"


def accidentDetected(colSnapshot , changes , readTime):
    global initial_load_complete
    global helmetID

    if not initial_load_complete:
        print(f"\nInitial Firestore Collection Snapshot loaded at {readTime}...")
        initial_load_complete = True
        return

    print(f"\nFirestore Collection Change Detected at {readTime}...")

    for change in changes:
        if change.type.name == 'ADDED':
            docData = change.document.to_dict()
            docId = change.document.id
            print(f"New document added: {docId}")

            if 'h_id' in docData:
                hId = docData['h_id']
                print(f"  Extracted h_id: {hId}")
                helmetID = hId
                if hId == hId:
                    print("Link Genarating Started...")
                    generate_dashboard_link_and_show_in_backend(purpose="initial_startup_link")
            else:
                print(f"  Document {docId} does not contain an 'h_id' field.")
        elif change.type.name == 'MODIFIED':
            pass
        elif change.type.name == 'REMOVED':
            pass

def massageSending(message: str):

    params = {
        "user_id": USER_ID,
        "api_key": API_KEY,
        "sender_id": SENDER_ID,
        "to": TO_NUMBER,
        "message": message
    }

    try:
        response = requests.get(url, params=params)

        if response.status_code == 200:
            print("SMS sent successfully!")
            print("Response:", response.text)
        else:
            print(f"Failed to send SMS. Status code: {response.status_code}")
            print("Response:", response.text)

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

@app.route('/api/validate_dashboard_access/<unique_token>', methods=['GET'])
def validate_dashboard_access(unique_token):
    print(f"Validation request for Dashboard Token: {unique_token}")
    if unique_token in unique_dashboard_access_tokens:
        token_info = unique_dashboard_access_tokens[unique_token]

        if datetime.now() > token_info['expires_at']:
            print(f"Dashboard token {unique_token} expired.")

            return jsonify({"message": "Access link has expired. Please request a new one."}), 401

        unique_dashboard_access_tokens[unique_token]['accessed'] = True
        print(f"Dashboard token {unique_token} validated successfully.")
        return jsonify({"status": "valid", "message": "Access granted."}), 200
    else:
        print(f"Invalid Dashboard Token: {unique_token}")
        return jsonify({"message": "Invalid dashboard access token. The link may be incorrect."}), 404



def generate_dashboard_link_and_show_in_backend(purpose="manual_generation"):
    unique_token = str(uuid.uuid4())
    unique_dashboard_access_tokens[unique_token] = {
        'purpose': purpose,
        'created_at': datetime.now(),
        'expires_at': datetime.now() + timedelta(minutes=60),
        'accessed': False
    }

    with app.test_request_context(base_url=REACT_FRONTEND_BASE_URL):

        unique_full_url = f"{REACT_FRONTEND_BASE_URL}/dashboard-access/{unique_token}"

    print(f"\n--- GENERATED UNIQUE DASHBOARD LINK ---")
    print(f"Purpose: {purpose}")
    print(f"Link: {unique_full_url}")
    print(f"Token: {unique_token}")
    print(f"Expires: {unique_dashboard_access_tokens[unique_token]['expires_at']}")
    print(f"-------------------------------------\n")
    print("Message Sending......")
    # massageSending(message=f"Access Website Using this Link: '{unique_full_url}'")

    return unique_full_url


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


# get heart beat from Real Time Database and save it to FireStore Vital Document with healmetId
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

#S Starting the realtime listener function
def startRealTimeDbLisner():
    print(f"[RTDB Listener] Starting Listener for path: {RTDB_LISTEN_PATH}...")

    try:
        realTimeDbRef.listen(realTimeDBListner)
        print("[RTDB Listener] Listener started successfully.")
    except Exception as e:
        print(f"[RTDB Listener] Listener terminated with error: {e}")
    print("[RTDB Listener] Listener stopped unexpectedly.")


if __name__ == '__main__':
    print("Starting Smart Helmet Backend Server...")

    # Set default environment variables for direct run
    os.environ.setdefault('FIREBASE_RTDB_URL', 'https://smarthelmet-3a072-default-rtdb.firebaseio.com/')
    os.environ.setdefault('FIREBASE_RTDB_LISTEN_PATH', '/')

    # Start the Firebase listener in a daemon thread
    listener_thread = threading.Thread(target=startRealTimeDbLisner, daemon=True)
    listener_thread.start()
    print("[RTDB Listener] Daemon thread for listener started.")

    # Start the Accident detection
    print(f"Listening for new documents in collection: '{COLLECTION_NAME}'...")
    colRef = firestoreDb.collection(COLLECTION_NAME)
    queryWatch = colRef.on_snapshot(accidentDetected)

    # print("Starting Flask application...")
    # generate_dashboard_link_and_show_in_backend(purpose="initial_startup_link")

    # Start Flask app (this will block the main thread)
    print("Starting Flask application on port 5000...")
    try:
        app.run(debug=False, port=5000)
    except KeyboardInterrupt:
        print("\nServer stopped by user.")
    except Exception as e:
        print(f"Flask app error: {e}")

    print("Application shutdown complete.")
