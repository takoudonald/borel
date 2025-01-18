from flask import Flask, request, jsonify

app = Flask(__name__)

# Stockage des SMS simulés
sms_inbox = []

@app.route('/send_sms', methods=['POST'])
def send_sms():
    data = request.get_json()
    numero = data.get("numero")
    message = data.get("message")
    print(f"SMS envoyé au {numero} : {message}")
    return jsonify({"status": "SMS envoyé avec succès"}), 200

@app.route('/read_sms', methods=['GET'])
def read_sms():
    return jsonify(sms_inbox), 200

@app.route('/add_sms', methods=['POST'])
def add_sms():
    data = request.get_json()
    sms_inbox.append(data)
    print(f"SMS ajouté : {data}")
    return jsonify({"status": "SMS ajouté"}), 200

if __name__ == "__main__":
    app.run(port=5000)
