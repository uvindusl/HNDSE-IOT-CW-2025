from flask import Flask, jsonify
from flask_cors import CORS
from itsdangerous import URLSafeTimedSerializer
import os
import firebase_admin
from firebase_admin import credentials, firestore , db


app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY' , '123')
serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
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
helmetID =  "h0222"

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

@app.route('/vitals' , methods=['GET'])
def getVitalDetails():
    vitalData = firestore_db.collection('Vitals').where('h_id', '==', helmetID)
    docs = vitalData.get()

    vitalData = []
    for doc in docs:
        vitalData.append(doc.to_dict())
    return jsonify(vitalData)




if __name__ == '__main__':
    app.run(debug=True , port=5000)
