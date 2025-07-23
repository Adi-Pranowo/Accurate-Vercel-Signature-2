from flask import Flask, request, jsonify
import hmac, hashlib, base64

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return "Signature API Ready!"

@app.route('/signature', methods=['POST'])
def signature():
    data = request.get_json()
    timestamp = data.get('timestamp')
    secret = data.get('secret')
    sig = hmac.new(secret.encode(), timestamp.encode(), hashlib.sha256).digest()
    return jsonify({"signature": base64.b64encode(sig).decode()})

app = app  # For Vercel
