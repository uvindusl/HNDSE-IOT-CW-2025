import firebase_admin
from firebase_admin import credentials , db , firestore
import threading
import os
import time

# Configuration for firebase
SERVICE_ACCOUNT_KEY_PATH = os.environ.get('FIREBASE_SERVICE_ACCOUNT_KEY', 'Key.json')
REALTIME_DATABASE_URL = os.environ.get('FIREBASE_RTDB_URL', 'https://smarthelmet-3a072-default-rtdb.firebaseio.com/')
RTDB_LISTEN_PATH = os.environ.get('FIREBASE_RTDB_LISTEN_PATH', '/')

realTimeDbRef = None
firestoreDb = None


# Initialize Firebase Admin SDK
def initializing():

    global realTimedbRef , firestoreDb

    if not firebase_admin._apps:
        try:
            cred = credentials.Certificate(SERVICE_ACCOUNT_KEY_PATH)
            firebase_admin.initialize_app(cred , {
            'databaseURL': REALTIME_DATABASE_URL
            })
            print('Firebase Admin SDK initialized.')
        except Exception as e:
            print(f"Error initializing Firebase Admin SDK: {e}")
            return False

    # Real time Database
    realTimeDbRef = db.reference(RTDB_LISTEN_PATH)

    # FireStore Database
    firestoreDb = firestore.client()

def realTimeDBListner(event):
    print(f"\n [RTDB Listener] Event Received: {event.event_type} at {event.path}")

    try:
        pathParts = [part for part in event.path.strip('/').split('/') if part]

        if firestoreDb is None:
            print("[RTDB Listener] Firestore DB not initialized. Skipping event processing.")
            return

        if len(pathParts) == 2 and pathParts[1] == 'heart_beat':
            documentId = pathParts[0]
            heartBeatValue = event.data

            firestoreCollectionName = 'Vitals'
            docRef = firestoreDb.collection(firestoreCollectionName).document(documentId)

            if event.event_type == 'put' or event.event_type == 'patch' :
                if heartBeatValue is not None:
                    newRecord = heartBeatValue

                    doc = docRef.get()

                    if doc.exists:
                        docData = doc.to_dict()
                        currentReadings = docData.get('heartbeat_readings', [])
                        currentReadings.append(newRecord)
                        docRef.update({'heartbeat_readings': currentReadings})

                        print(f"[RTDB Listener] Appended new heartbeat to '{documentId}' in '{firestoreCollectionName}' .")
                    else:
                        docRef.set({
                            'heartbeat_readings': [newRecord],
                            'h_id': documentId,
                        })
                        print(f"[RTDB Listener] Created new document '{documentId} in '{firestoreCollectionName}' .")
                else:
                    print(f"[RTDB Listener] heartbeat child for '{documentId}' was set to None (deleted) . ")
            else:
                print(f"[RTDB Listener] Unhandled event type for heart_beat: {event.event_type} ")

        else:
            print(f"[RTDB Listener] Path '{event.path}' does not match expected '/{{hxxx}}/heart_beat' pattern. Skipping")
    except Exception as e:
        print(f"[RTDB Listener] Error processing Realtime Database event: {e}")

def startRealTimeDbLisner():
    global realTimeDbRef

    if realTimeDbRef is None:
        print("[RTDB Listener] Realtime DB reference not initialized. Cannot start listener.")
        return

    print(f"[RTDB Listener] Starting Listener for path: {RTDB_LISTEN_PATH}...")
    try:
        realTimeDbRef.listen(realTimeDBListner)
    except Exception as e:
        print(f"[RTDB Listener] Listener terminated with error: {e}")
    print("[RTDB Listener] Listener stopped unexpectedly.")


# if __name__ == '__main__':
#     print("Running rtdb_sync.py directly for testing listener.")
#     # Initialize again if not already (important for direct run)
#     if not firebase_admin._apps:
#         try:
#             cred = credentials.Certificate(SERVICE_ACCOUNT_KEY_PATH)
#             firebase_admin.initialize_app(cred, {
#                 'databaseURL': REALTIME_DATABASE_URL
#             })
#             print("Firebase Admin SDK initialized for direct run.")
#         except Exception as e:
#             print(f"Error initializing Firebase for direct run: {e}")
#             exit(1)
#
#     os.environ.setdefault('FIREBASE_RTDB_URL', 'https://smarthelmet-3a072-default-rtdb.firebaseio.com/')
#     os.environ.setdefault('FIREBASE_RTDB_LISTEN_PATH', '/')
#
#     if not os.environ.get('FIREBASE_RTDB_URL') or not os.environ.get('FIREBASE_RTDB_LISTEN_PATH'):
#         print(
#             "Please set FIREBASE_RTDB_URL and FIREBASE_RTDB_LISTEN_PATH environment variables or update hardcoded values for direct run.")
#         exit(1)
#
#     listener_thread = threading.Thread(target=startRealTimeDbLisner, daemon=True)
#     listener_thread.start()
#     print("[RTDB Listener] Daemon thread for listener started.")
#
#     try:
#         print("Press Ctrl+C to stop the listener and exit...")
#         while True:
#             time.sleep(1)
#     except KeyboardInterrupt:
#         print("\nExiting listener due to KeyboardInterrupt.")
#     except Exception as e:
#         print(f"An unexpected error occurred in the main thread: {e}")
#
#     print("Main thread exiting.")