from flask import Flask, request, jsonify, url_for, redirect, render_template_string
from flask_cors import CORS
from google.oauth2.gdch_credentials import SERVICE_ACCOUNT_TOKEN_TYPE
from google.protobuf.proto import serialize
from itsdangerous import URLSafeTimedSerializer
import os
import time
import threading
import firebase_admin
from firebase_admin import credentials, firestore , db


app = Flask(__name__)
CORS(app)
# cred = credentials.Certificate("key.json")
# firebase_admin.initialize_app(cred)
# db= firestore.client()
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY' , '123')
serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
#
#
# cred = credentials.Certificate("path/to/serviceAccountKey.json")
# firebase_admin.initialize_app(cred)
#
# cred_obj = firebase_admin.credentials.Certificate('key.json')
# default_app = firebase_admin.initialize_app(cred_obj, {
#     'databaseURL':"https://smarthelmet-3a072-default-rtdb.firebaseio.com/"
#     })
#
# ref = db.reference("/")
# print(ref.order_by_child("Price").get())

# Initialize Firebase
SERVICE_ACCOUNT_KEY_PATH = 'key.json'
REAL_TIME_DATABASE = 'https://smarthelmet-3a072-default-rtdb.firebaseio.com/'

# Initialize Firebase Admin SDK
try:
    cred = credentials.Certificate(SERVICE_ACCOUNT_KEY_PATH)
    firebase_admin.initialize_app(cred, {
        'databaseURL': REAL_TIME_DATABASE
    })
    print('Firebase Admin SDK initialized')
except Exception as e:
    print(e)

firestore_db = firestore.client()

realtime_db_ref = db.reference('/')

#this will be change in future it will come to backend from mobile app or firebase idk
helmetID =  "h002"

@app.route('/riders', methods=['GET'])
def getRiderDetails():
    riderData = firestore_db.collection('Riders').where('h_id', '==', helmetID)
    docs = riderData.get()

    riderData = []
    for doc in docs:
        riderData.append(doc.to_dict())
    return jsonify(riderData)

@app.route('/accidents', methods=['GET'])
def getAccidentDetails():
    accidentData = firestore_db.collection('Accidents').where('h_id', '==', helmetID)
    docs = accidentData.get()

    accidentData = []
    for doc in docs:
        accidentData.append(doc.to_dict())
    return jsonify(accidentData)

# @app.route('/accidentdatas' , methods=['GET'])
# def getAccidentDatas():
#     accidentDatas = db.collection('Accident_Data').where('h_id', '==', helmetID)
#     docs = accidentDatas.get()
#
#     accidentDatas = []
#     for doc in docs:
#         accidentDatas.append(doc.to_dict())
#     return jsonify(accidentDatas)

@app.route('/vitals' , methods=['GET'])
def getVitalDetails():
    vitalData = firestore_db.collection('Vitals').where('h_id', '==', helmetID)
    docs = vitalData.get()

    vitalData = []
    for doc in docs:
        vitalData.append(doc.to_dict())
    return jsonify(vitalData)

@app.route('/heartbeat', methods=['GET'])
def getData():
    try:
        messages = realtime_db_ref.get()
        # Realtime Database returns a dictionary, convert to list of dicts if needed for typical JSON API response
        if messages:
            # Convert the dictionary of messages to a list for easier consumption in a frontend
            message_list = [{"id": key, **value} for key, value in messages.items()]
            return jsonify(message_list), 200
        else:
            return jsonify([]), 200
    except Exception as e:
        return jsonify({"error": f"Error getting messages from Realtime Database: {e}"}), 500


if __name__ == '__main__':
    app.run(debug=True , port=5000)

