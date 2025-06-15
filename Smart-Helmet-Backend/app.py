from flask import Flask, request, jsonify
from flask_cors import CORS
import secrets
import time

app = Flask(__name__)
tokens = {}  # temporary token storage
CORS("http://localhost:5173/")

@app.route('/')
def generate_token():
    token = secrets.token_urlsafe(32)
    expiration_time = time.time() + 3600
    tokens[token] = expiration_time
    return jsonify({'token' : token})

@app.route('/validate_token/<token>', methods=['GET'])
def validate_token(token):
    if token in tokens:
        if tokens[token] > time.time():
            del tokens[token]
            return jsonify({'message': 'Token valid'})
        else:
            del tokens[token]
            return jsonify({'message': 'Token expired'}), 401
    else:
        return jsonify({'message': 'Invalid token'}), 401

@app.route('/dashboard_data', methods=['GET'])
def dashboard_data():
    # Fetch dashboard data
    data = {'message': 'Dashboard data fetched'}
    return jsonify(data)


if __name__ == '__main__':
    app.run()
