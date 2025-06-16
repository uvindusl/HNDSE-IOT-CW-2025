from flask import Flask, request, jsonify
from flask_cors import CORS
import secrets
import time
import firebase_admin
from firebase_admin import credentials, firestore


app = Flask(__name__)
CORS(app)
cred = credentials.Certificate("key.json")
firebase_admin.initialize_app(cred)
db= firestore.client()

riderNic =  "0384328472"

@app.route('/users/data', methods=['GET'])
def get_users():
    users_ref = db.collection('Riders').where('NIC', '==', riderNic)
    docs = users_ref.get()

    user_list = []
    for doc in docs:
        user_list.append(doc.to_dict())
    return jsonify(user_list)



if __name__ == '__main__':
    app.run(debug=True , port=5000)
