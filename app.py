import hashlib

from flask import Flask, request, jsonify

app = Flask(__name__)

# Predefined list of banned HWIDs (for testing, can later be stored in a database)
banned_hwids = [
    "8aef14195b8ae56620caeaf83df34b532253709851997fbabd3454676092f238", 
    "MP27RYCQ0025_38D3_21D1_FE29.MP27RYCQBFEBFBFF000806C2C4:75:AB:3B:13:DE"
]

def get_hwid():
    # Simulate getting a hardware ID for testing purposes
    hwid = "SIMULATED_HARDWARE_ID_FOR_TESTING"
    return hwid

def hash_hwid(hwid):
    return hashlib.sha256(hwid.encode()).hexdigest()

def is_banned(hwid):
    hashed_hwid = hash_hwid(hwid)
    return hashed_hwid in banned_hwids

@app.route('/check_hwid', methods=['POST'])
def check_hwid():
    data = request.get_json()
    hwid = get_hwid()  # Retrieve the user's hardware ID

    if is_banned(hwid):
        return jsonify({"status": "banned", "hwid": hwid}), 403
    else:
        return jsonify({"status": "allowed", "hwid": hwid}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
