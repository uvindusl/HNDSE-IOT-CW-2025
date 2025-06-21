import firebase_admin
from firebase_admin import credentials, db, firestore
import threading
import os
import time

# Configuration for firebase
SERVICE_ACCOUNT_KEY_PATH = os.environ.get('FIREBASE_SERVICE_ACCOUNT_KEY', 'Key.json')
REALTIME_DATABASE_URL = os.environ.get('FIREBASE_RTDB_URL', 'https://smarthelmet-3a072-default-rtdb.firebaseio.com/')
RTDB_LISTEN_PATH = os.environ.get('FIREBASE_RTDB_LISTEN_PATH', '/')

# Initialize Firebase Admin SDK
if not firebase_admin._apps:
    try:
        cred = credentials.Certificate(SERVICE_ACCOUNT_KEY_PATH)
        firebase_admin.initialize_app(cred, {
            'databaseURL': REALTIME_DATABASE_URL
        })
        print("Firebase Admin SDK initialized.")
    except Exception as e:
        print(f"Error initializing Firebase Admin SDK: {e}")

rtdb_ref = db.reference(RTDB_LISTEN_PATH)
firestore_db = firestore.client()

def rtdb_listner(event):
    print(f"\n[RTDB Listener] Event Received: {event.event_type} at {event.path}")

    try:
        path_parts = [part for part in event.path.strip('/').split('/') if part]

        if len(path_parts) == 2 and path_parts[1] == 'heart_beat':
            document_id = path_parts[0]
            heart_beat_value = event.data

            firestore_collection_name = 'Vitals'
            doc_ref = firestore_db.collection(firestore_collection_name).document(document_id)

            if event.event_type == 'put' or event.event_type == 'patch' :
                if heart_beat_value is not None:
                    new_reading = heart_beat_value
                    # new_reading = {
                    #     'value' : heart_beat_value,
                    #     'timestamp' : datetime.now()
                    # }

                    doc = doc_ref.get()

                    if doc.exists:
                        doc_data = doc.to_dict()
                        current_readings = doc_data.get('heartbeat_readings',[])
                        current_readings.append(new_reading)
                        doc_ref.update({'heartbeat_readings': current_readings})
                        print(f"[RTDB Listener] Appended new heartbeat to '{document_id}' in '{firestore_collection_name}'.")
                    else :
                        doc_ref.set({
                            'heartbeat_readings': [new_reading],
                            'h_id': document_id,
                        })
                        print(f"[RTDB Listener] Created new document '{document_id}' in '{firestore_collection_name}' with first heartbeat.")
                else :
                    print(f"[RTDB Listener] heart_beat child for '{document_id}' was set to None (deleted).")
            else:
                print(f"[RTDB Listener] Unhandled event type for heart_beat: {event.event_type}")

        else:
            print(f"[RTDB Listener] Path '{event.path}' does not match expected '/{{hXXX}}/heart_beat' pattern. Skipping.")

    except Exception as e:
        print(f"[RTDB Listener] Error processing Realtime Database event: {e}")


def start_rtdb_listener():
    """
    Starts the Realtime Database listener. This function is blocking.
    """
    print(f"[RTDB Listener] Starting listener for path: {RTDB_LISTEN_PATH}...")
    try:
        rtdb_ref.listen(rtdb_listner)
    except Exception as e:
        print(f"[RTDB Listener] Listener terminated with error: {e}")
    print("[RTDB Listener] Listener stopped unexpectedly.")


def get_firestore_client():
    """
    Returns the initialized Firestore client.
    """
    return firestore_db



def get_heartbeat_data_from_firestore(doc_id):
    try:
        doc_ref = firestore_db.collection('Vitals').document(doc_id)
        doc = doc_ref.get()
        if doc.exists:
            data = doc.to_dict()
            print(f"[Firestore Util] Retrieved heartbeat data for '{doc_id}': {data}")
            return data
        else:
            print(f"[Firestore Util] Heartbeat data for '{doc_id}' not found.")
            return None
    except Exception as e:
        print(f"[Firestore Util] Error retrieving heartbeat data for '{doc_id}': {e}")
        return None

if __name__ == '__main__':
    print("Running rtdb_sync.py directly for testing listener.")
    # Initialize again if not already (important for direct run)
    if not firebase_admin._apps:
        try:
            cred = credentials.Certificate(SERVICE_ACCOUNT_KEY_PATH)
            firebase_admin.initialize_app(cred, {
                'databaseURL': REALTIME_DATABASE_URL
            })
            print("Firebase Admin SDK initialized for direct run.")
        except Exception as e:
            print(f"Error initializing Firebase for direct run: {e}")
            exit(1)

    os.environ.setdefault('FIREBASE_RTDB_URL', 'https://smarthelmet-3a072-default-rtdb.firebaseio.com/')
    os.environ.setdefault('FIREBASE_RTDB_LISTEN_PATH', '/')


    if not os.environ.get('FIREBASE_RTDB_URL') or not os.environ.get('FIREBASE_RTDB_LISTEN_PATH'):
        print("Please set FIREBASE_RTDB_URL and FIREBASE_RTDB_LISTEN_PATH environment variables or update hardcoded values for direct run.")
        exit(1)

    listener_thread = threading.Thread(target=start_rtdb_listener, daemon=True)
    listener_thread.start()
    print("[RTDB Listener] Daemon thread for listener started.")

    try:
        print("Press Ctrl+C to stop the listener and exit...")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nExiting listener due to KeyboardInterrupt.")
    except Exception as e:
        print(f"An unexpected error occurred in the main thread: {e}")

    print("Main thread exiting.")