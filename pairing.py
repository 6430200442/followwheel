from flask import Flask, request, jsonify

app = Flask(__name__)
owner_mac = None  # เก็บ MAC Address ของเจ้าของชั่วคราว

@app.route('/register', methods=['POST'])
def register():
    global owner_mac
    owner_mac = request.json.get("mac_address")
    return {"status": "success", "mac": owner_mac}

@app.route('/owner', methods=['GET'])
def get_owner():
    if owner_mac:
        return jsonify({"owner_mac": owner_mac})
    else:
        return jsonify({"error": "No owner registered"}), 404

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
