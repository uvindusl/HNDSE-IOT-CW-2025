from flask import Flask, request, jsonify, url_for, redirect, render_template_string
from flask_cors import CORS
from google.protobuf.proto import serialize
from itsdangerous import URLSafeTimedSerializer
import os
import datetime
import firebase_admin
from firebase_admin import credentials, firestore


app = Flask(__name__)
CORS(app)
cred = credentials.Certificate("key.json")
firebase_admin.initialize_app(cred)
db= firestore.client()
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY' , '123')
serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

#this will be change in future it will come to backend from mobile app or firebase idk
helmetID =  "h0222"

@app.route('/riders', methods=['GET'])
def getRiderDetails():
    riderData = db.collection('Riders').where('h_id', '==', helmetID)
    docs = riderData.get()

    riderData = []
    for doc in docs:
        riderData.append(doc.to_dict())
    return jsonify(riderData)

@app.route('/accidents', methods=['GET'])
def getAccidentDetails():
    accidentData = db.collection('Accidents').where('h_id', '==', helmetID)
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
    vitalData = db.collection('Vitals').where('h_id', '==', helmetID)
    docs = vitalData.get()

    vitalData = []
    for doc in docs:
        vitalData.append(doc.to_dict())
    return jsonify(vitalData)

if __name__ == '__main__':
    app.run(debug=True , port=5000)
