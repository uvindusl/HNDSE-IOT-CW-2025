from flask import Flask, jsonify
from flask_cors import CORS
import threading
import os
import firebase_admin
from firebase_admin import credentials, firestore , db
import uuid
from datetime import datetime , timedelta
import requests
from dotenv import load_dotenv
import logging

app = Flask(__name__)

# This is for connect backend with frontend
CORS(app)
load_dotenv()

# Configuration for firebase
SERVICE_ACCOUNT_KEY_PATH = os.environ.get('FIREBASE_SERVICE_ACCOUNT_KEY', 'key.json')
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

# Global Variable to store h_id coming from detect change function
helmetID =  None

# Configure basic logging (can be more advanced)
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# Configuration for the unique URL genaration
REACT_FRONTEND_BASE_URL = "https://hndseiotcw2025.vercel.app"
dashboardAccessTokens = {}

# Notify.lk APIs
USER_ID = os.getenv('USER_ID')
API_KEY = os.getenv('API_KEY')
TO_NUMBER = "94702004065"
SENDER_ID = "NotifyDEMO"
url = os.getenv('URL')

# Accident Detection Function
def accidentDetected(colSnapshot , changes , readTime):

    # Intents for Global Variable
    global initial_load_complete
    global helmetID

    if not initial_load_complete:
        print(f"\nInitial Firestore Collection Snapshot loaded at {readTime}...")
        initial_load_complete = True
        return

    print(f"\nFirestore Collection Change Detected at {readTime}...")

    for change in changes:
        if change.type.name == 'ADDED':
            # Convert the document snapshot to a dictionary
            docData = change.document.to_dict()
            # get Change document Id
            docId = change.document.id
            # printing document Id
            print(f"New document added: {docId}")

            # Verifying 'h_id' is in document
            if 'h_id' in docData:
                # assign h_id to Variable
                hId = docData['h_id']
                # Print h_id
                print(f"  Extracted h_id: {hId}")
                helmetID = hId # assigning hId into global Variable
                if hId == hId: # if h_id is there Start Generating Link
                    print("Link Generating Started...")
                    generateUniqueUrl(purpose="initial_startup_link") # start generateUniqueUrl function and pass purpose parameter 'initial_startup_link'

            else:
                print(f"Document {docId} does not contain an 'h_id' field.") # if h_id doesn't there print this
        elif change.type.name == 'MODIFIED':
            pass # if document modified it will pass
        elif change.type.name == 'REMOVED':
            pass # if document remove it also pass

# massage Sending Function that get parameter message
def massageSending(message: str):

    # array to store params in url
    params = {
        "user_id": USER_ID,
        "api_key": API_KEY,
        "sender_id": SENDER_ID,
        "to": TO_NUMBER,
        "message": message
    }

    try:
        response = requests.get(url, params=params) # Sending request to Notify.lk

        if response.status_code == 200: # if message successfully send print message with response text
            print("SMS sent successfully!")
            print("Response:", response.text)
        else:
            print(f"Failed to send SMS. Status code: {response.status_code}") # if there is any array print this
            print("Response:", response.text)

    except requests.exceptions.RequestException as e: # Exception handling
        print(f"An error occurred: {e}")

# function to send token data and send status code
@app.route('/validateDashboardAccess/<uniqueToken>', methods=['GET'])
def validateDashboardAccess(uniqueToken):
    print(f"Validation request for Dashboard Token: {uniqueToken}") # validating Token
    if uniqueToken in dashboardAccessTokens:
        tokenInfo = dashboardAccessTokens[uniqueToken]

        if datetime.now() > tokenInfo['expires_at']: # check is token expire or not
            print(f"Dashboard token {uniqueToken} expired.")

            return jsonify({"message": "Access link has expired. Please request a new one."}), 401

        dashboardAccessTokens[uniqueToken]['accessed'] = True
        print(f"Dashboard token {uniqueToken} validated successfully.")
        return jsonify({"status": "valid", "message": "Access granted."}), 200
    else:
        print(f"Invalid Dashboard Token: {uniqueToken}")
        return jsonify({"message": "Invalid dashboard access token. The link may be incorrect."}), 404


# function for Generating unique id and show it on backend
def generateUniqueUrl(purpose="manual_generation"):
    uniqueToken = str(uuid.uuid4()) # generate universal unique identifier for url
    dashboardAccessTokens[uniqueToken] = { # Save generated token details
        'purpose': purpose,
        'created_at': datetime.now(),
        'expires_at': datetime.now() + timedelta(minutes=60),
        'accessed': False
    }

    with app.test_request_context(base_url=REACT_FRONTEND_BASE_URL):
        uniqueFullUrl = f"{REACT_FRONTEND_BASE_URL}/dashboard-access/{uniqueToken}"

    print(f"\n--- GENERATED UNIQUE DASHBOARD LINK ---") # printing generated link details
    print(f"Purpose: {purpose}")
    print(f"Link: {uniqueFullUrl}")
    print(f"Token: {uniqueToken}")
    print(f"Expires: {dashboardAccessTokens[uniqueToken]['expires_at']}")
    print(f"-------------------------------------\n")

    logger.info("--- GENERATED UNIQUE DASHBOARD LINK ---")
    logger.info(f"Purpose: {purpose}")
    logger.info(f"Link: {uniqueFullUrl}")
    logger.info(f"Token: {uniqueToken}")
    logger.info(f"Expires: {dashboardAccessTokens[uniqueToken]['expires_at']}")
    logger.info("-------------------------------------")

    # print("---Message Sending---\n")
    # massageSending(message=f"Accident detected you can get details by visiting this WebSite : '{uniqueFullUrl}'")

    return uniqueFullUrl

# Get methods for the get data from firebase
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


# get heart beat from Real Time Database and save it to FireStore Vital Document with helmet Id
def realTimeDBListner(event):
    print(f"\n[RTDB Listener] Event Received: {event.event_type} at {event.path}")

    try:
        pathParts = [part for part in event.path.strip('/').split('/') if part] # remove spaces and get data as array using split function

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

# Starting the realtime listener function
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

    # Start Flask app (this will block the main thread)
    port = int(os.environ.get("PORT", 8080))
    print(f"Starting Flask application on port {port}...")
    try:
        app.run(port=port , host="0.0.0.0")
    except KeyboardInterrupt:
        print("\nServer stopped by user.")
    except Exception as e:
        print(f"Flask app error: {e}")

    print("Application shutdown complete.")
