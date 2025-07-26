from flask import Flask, request, jsonify
import hmac
import hashlib
import base64

app = Flask(__name__)

@app.route('/signature', methods=['POST'])
def signature():
    # Ambil JSON payload dari POST request
    data = request.get_json(force=True, silent=True)
    if not data:
        return jsonify({"error": "No JSON body received"}), 400

    # Ambil parameter utama
    secret = data.get('secret')
    method = data.get('method')
    path = data.get('path')
    timestamp = data.get('timestamp')
    if not all([secret, method, path, timestamp]):
        return jsonify({"error": "parameter missing"}), 400

    # Susun string: "{METHOD}:{PATH}:{TIMESTAMP}"
    message = f"{method}:{path}:{timestamp}"
    # HMAC-SHA256, hasil BASE64
    sig = hmac.new(secret.encode(), message.encode(), hashlib.sha256).digest()
    signature = base64.b64encode(sig).decode()
    return jsonify({"signature": signature})

app = app  # Penting untuk deployment di Vercel

