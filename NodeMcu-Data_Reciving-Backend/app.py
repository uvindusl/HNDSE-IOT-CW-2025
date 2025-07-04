from flask import Flask, request, jsonify
import os
import firebase_admin
from firebase_admin import credentials, db
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

SERVICE_ACCOUNT_KEY_PATH = os.environ.get('FIREBASE_SERVICE_ACCOUNT_KEY', 'key.json')
REALTIME_DATABASE_URL = os.environ.get('FIREBASE_RTDB_URL', 'https://smarthelmet-3a072-default-rtdb.firebaseio.com/')

if not firebase_admin._apps:
    try:
        cred = credentials.Certificate(SERVICE_ACCOUNT_KEY_PATH)
        firebase_admin.initialize_app(cred, {
            'databaseURL': REALTIME_DATABASE_URL
        })
        logger.info('Firebase Admin SDK initialized successfully.')
        exit(1)
    except Exception as e:
        logger.error(f"Error initializing Firebase Admin SDK: {e}")
        exit(1)


@app.route('/nodemcu', methods=['POST'])
def receive_data_from_nodemcu():
    if not request.is_json:
        return jsonify({"status": "error", "message": "Request must be JSON"}), 400

    data = request.json
    logger.info(f"Received JSON data: {data}")

    helmetId = data.get('hid')
    heartBeat = int(data.get('heartbeat'))

    if not helmetId:
        return jsonify({"status": "error", "message": "'hid' (helmet ID) is required."}), 400
    if heartBeat is None:
        return jsonify({"status": "error", "message": "'value' (heart beat) is required."}), 400

    try:
        helmet_readings_ref = db.reference(helmetId)

        new_record_ref = helmet_readings_ref.set({
            'heart_beat': heartBeat,
        })

        logger.info(f"Heart beat {heartBeat} saved for helmet ID: {helmetId}.")

        return jsonify({
            "status": "success",
            "message": f"Heart beat for {helmetId} saved successfully!",
            "helmet_id": helmetId,
            "heart_beat": heartBeat,
        }), 201

    except Exception as e:
        logger.exception(f"Error saving data for helmet ID {helmetId} to Firebase:")
        return jsonify({
            "status": "error",
            "message": f"Failed to save data to Firebase: {str(e)}"
        }), 500


if __name__ == '__main__':

    os.environ.setdefault('FIREBASE_RTDB_URL', 'https://smarthelmet-3a072-default-rtdb.firebaseio.com/')

    port = int(os.environ.get("PORT", 8080))
    logger.info(f"Starting Flask app on : {port}")

    try:
        app.run(host="0.0.0.0", port=port)
    except KeyboardInterrupt:
        logger.info("Server stopped by user (KeyboardInterrupt).")
    except Exception as e:
        logger.critical(f"Flask app crashed: {e}")