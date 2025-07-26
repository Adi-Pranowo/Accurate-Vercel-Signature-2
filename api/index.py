from flask import Flask, request, jsonify
import hmac, hashlib, base64

app = Flask(__name__)

# Route default (opsional, untuk cek "alive")
@app.route('/', methods=['GET'])
def home():
    return "Signature API Ready!"

# Route utama signature
@app.route('/api/signature', methods=['POST'])
def signature():
    # Get JSON body
    data = request.get_json(force=True, silent=True)
    if not data:
        return jsonify({"error": "No JSON body received"}), 400

    secret = data.get('secret')
    method = data.get('method')
    path = data.get('path')
    timestamp = data.get('timestamp')

    # Cek parameter lengkap
    if not all([secret, method, path, timestamp]):
        return jsonify({"error": "parameter missing"}), 400

    message = f"{method}:{path}:{timestamp}"
    sig = hmac.new(secret.encode(), message.encode(), hashlib.sha256).digest()
    signature = base64.b64encode(sig).decode()

    return jsonify({"signature": signature})

# Agar flask app terdeteksi vercel-python
app = app
