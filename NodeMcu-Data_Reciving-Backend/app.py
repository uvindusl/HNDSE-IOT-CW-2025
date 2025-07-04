from flask import Flask , request , jsonify
import os
import firebase_admin
from firebase_admin import credentials, firestore , db

app = Flask(__name__)

# Configuration for firebase
SERVICE_ACCOUNT_KEY_PATH = os.environ.get('FIREBASE_SERVICE_ACCOUNT_KEY', 'key.json')
REALTIME_DATABASE_URL = os.environ.get('FIREBASE_RTDB_URL', 'https://smarthelmet-3a072-default-rtdb.firebaseio.com/')
RTDB_LISTEN_PATH = os.environ.get('FIREBASE_RTDB_LISTEN_PATH', '/')


initial_load_complete = False

helmetId = None
heatBeat = None

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

@app.route('/nodemcu', methods=['POST'])
def receviedDataFromNodeMcu():
    global helmetId
    global heatBeat

    if request.is_json:

        data = request.json
        print(f"Received JSON data: {data}")

        helmetId = data.get('hid')
        heatBeat = data.get('value')
        if helmetId is None or heatBeat is None:
            return jsonify({"status": "success", "message": "Data received successfully!"}), 200

        try:
            newRef = db.reference(helmetId)

            ref = newRef.push({
                'heart_beat': heatBeat
            })
        except Exception as e:
            print(f"Error updating helmet ID: {e}")

        return jsonify({"status": "success", "message": "Data received successfully!"}), 200


    else:
        return jsonify({"status": "error", "message": "Request must be JSON"}), 400


if __name__ == '__main__':

    # Set default environment variables for direct run
    os.environ.setdefault('FIREBASE_RTDB_URL', 'https://smarthelmet-3a072-default-rtdb.firebaseio.com/')
    os.environ.setdefault('FIREBASE_RTDB_LISTEN_PATH', '/')


    port = int(os.environ.get("PORT", 8080))
    try:
        app.run(port=port , host="0.0.0.0")
    except KeyboardInterrupt:
        print("\nServer stopped by user.")
    except Exception as e:
        print(f"Flask app error: {e}")
