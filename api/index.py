from flask import Flask, request, jsonify
import hmac, hashlib, base64

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return "Signature API Ready!"

@app.route('/signature', methods=['POST'])
def signature():
    data = request.get_json(force=True, silent=True)
    if not data:
        data = request.form or request.values or None
    if not data:
        return jsonify({"error": "No JSON body received"}), 400

    secret = data.get('secret')
    method = data.get('method')
    path = data.get('path')
    timestamp = data.get('timestamp')
    if not all([secret, method, path, timestamp]):
        return jsonify({"error": "parameter missing"}), 400

    message = f"{method}:{path}:{timestamp}"
    sig = hmac.new(secret.encode(), message.encode(), hashlib.sha256).digest()
    return jsonify({"signature": base64.b64encode(sig).decode()})

app = app
