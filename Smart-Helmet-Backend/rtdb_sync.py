# rtdb_sync.py

import firebase_admin
from firebase_admin import credentials, db, firestore
from datetime import datetime # Correct import for datetime.now()
import threading
import os
import time # <-- Add this import

# --- Configuration (better to load from environment variables in production) ---
SERVICE_ACCOUNT_KEY_PATH = os.environ.get('FIREBASE_SERVICE_ACCOUNT_KEY', 'Key.json')
REALTIME_DATABASE_URL = os.environ.get('FIREBASE_RTDB_URL', 'https://smarthelmet-3a072-default-rtdb.firebaseio.com/')
RTDB_LISTEN_PATH = os.environ.get('FIREBASE_RTDB_LISTEN_PATH', '/')

# Initialize Firebase Admin SDK (only once)
if not firebase_admin._apps:
    try:
        cred = credentials.Certificate(SERVICE_ACCOUNT_KEY_PATH)
        firebase_admin.initialize_app(cred, {
            'databaseURL': REALTIME_DATABASE_URL
        })
        print("Firebase Admin SDK initialized.")
    except Exception as e:
        print(f"Error initializing Firebase Admin SDK: {e}")
        # Depending on your app, you might want to exit or handle gracefully
        # For now, we'll let it continue but the listener won't work.

rtdb_ref = db.reference(RTDB_LISTEN_PATH)
firestore_db = firestore.client()

def rtdb_listner(event): # Typo: listner should be listener (consistent with comments)
    print(f"\n[RTDB Listener] Event Received: {event.event_type} at {event.path}")

    try:
        path_parts = [part for part in event.path.strip('/').split('/') if part]

        # Your Realtime Database structure is directly h001/heart_beat, so the parent path is '/'
        # When event.path is '/h001/heart_beat', path_parts will be ['h001', 'heart_beat']
        # This condition correctly checks for that.
        if len(path_parts) == 2 and path_parts[1] == 'heart_beat':
            document_id = path_parts[0] # This will be 'h001', 'h002', etc.
            heart_beat_value = event.data

            # Firestore collection name where you want to store this data
            firestore_collection_name = 'Vitals' # Changed to 'Vitals' as per your code
            doc_ref = firestore_db.collection(firestore_collection_name).document(document_id)

            if event.event_type == 'put' or event.event_type == 'patch' :
                if heart_beat_value is not None:
                    new_reading = {
                        'value' : heart_beat_value,
                        'timestamp' : datetime.now() # Use datetime.now()
                    }

                    doc = doc_ref.get() # Use 'doc' instead of 'docs' for clarity

                    if doc.exists:
                        doc_data = doc.to_dict()
                        current_readings = doc_data.get('heartbeat_readings', [])
                        current_readings.append(new_reading)
                        doc_ref.update({'heartbeat_readings': current_readings})
                        print(f"[RTDB Listener] Appended new heartbeat to '{document_id}' in '{firestore_collection_name}'.")
                    else :
                        doc_ref.set({
                            'heartbeat_readings': [new_reading],
                            'last_updated': datetime.now() # Use datetime.now()
                        })
                        print(f"[RTDB Listener] Created new document '{document_id}' in '{firestore_collection_name}' with first heartbeat.")
                else :
                    # If heart_beat_value is None, it implies deletion of 'heart_beat' child
                    print(f"[RTDB Listener] heart_beat child for '{document_id}' was set to None (deleted).")
                    # You might want to remove the document from Firestore or clear the array here
                    # Example: doc_ref.delete() if the entire hXXX document should be removed
                    # Or: doc_ref.update({'heartbeat_readings': firestore.ArrayRemove(...)}) if removing specific reading
                    # For now, it just logs.
            else:
                print(f"[RTDB Listener] Unhandled event type for heart_beat: {event.event_type}")

        else:
            # This will catch the initial 'put' event at '/', and any other paths not matching /hXXX/heart_beat
            print(f"[RTDB Listener] Path '{event.path}' does not match expected '/{{hXXX}}/heart_beat' pattern. Skipping.")

    except Exception as e:
        print(f"[RTDB Listener] Error processing Realtime Database event: {e}")


def start_rtdb_listener():
    """
    Starts the Realtime Database listener. This function is blocking.
    """
    print(f"[RTDB Listener] Starting listener for path: {RTDB_LISTEN_PATH}...") # Use RTDB_LISTEN_PATH here
    try:
        # The listener will keep running indefinitely in its thread
        rtdb_ref.listen(rtdb_listner) # Use rtdb_listner
    except Exception as e:
        print(f"[RTDB Listener] Listener terminated with error: {e}")
    # This line below will only be reached if listen() somehow stops (e.g., connection error, Firebase credential issue)
    print("[RTDB Listener] Listener stopped unexpectedly.")


def get_firestore_client():
    """
    Returns the initialized Firestore client.
    """
    return firestore_db


# Example of a function to retrieve data from Firestore
def get_heartbeat_data_from_firestore(doc_id):
    try:
        doc_ref = firestore_db.collection('Vitals').document(doc_id) # Use 'Vitals' collection
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
            exit(1) # Exit if Firebase init fails for direct run

    # Set some dummy env vars for direct testing if they aren't set
    # MAKE SURE THESE ARE CORRECT FOR YOUR DATABASE:
    os.environ.setdefault('FIREBASE_RTDB_URL', 'https://smarthelmet-3a072-default-rtdb.firebaseio.com/')
    os.environ.setdefault('FIREBASE_RTDB_LISTEN_PATH', '/')

    # Ensure Realtime DB URL and path are set for testing
    if not os.environ.get('FIREBASE_RTDB_URL') or not os.environ.get('FIREBASE_RTDB_LISTEN_PATH'):
        print("Please set FIREBASE_RTDB_URL and FIREBASE_RTDB_LISTEN_PATH environment variables or update hardcoded values for direct run.")
        exit(1) # Exit if essential config is missing

    # Start the listener in a separate daemon thread
    listener_thread = threading.Thread(target=start_rtdb_listener, daemon=True)
    listener_thread.start()
    print("[RTDB Listener] Daemon thread for listener started.")

    try:
        print("Press Ctrl+C to stop the listener and exit...")
        # Keep the main thread alive indefinitely, catching KeyboardInterrupt
        while True:
            time.sleep(1) # Sleep to prevent busy-waiting and allow daemon threads to run
    except KeyboardInterrupt:
        print("\nExiting listener due to KeyboardInterrupt.")
    except Exception as e:
        print(f"An unexpected error occurred in the main thread: {e}")

    print("Main thread exiting.")