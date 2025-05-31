from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "Welcome to the Knowledge API! Visit /knowledge to get data."

@app.route("/knowledge", methods=["GET"])
def get_knowledge():
    data = {
        "progetti": [
            {
                "nome": "Finance for Schools",
                "partner": ["Italiacamp", "Starting Finance"],
                "target": "Scuole secondarie",
                "note": "Seminari + contenuti digitali"
            }
        ],
        "governance": {
            "presidente": "Davide Franchini",
            "CTS": ["Marcella Panucci", "Matteo Petrella"]
        },
        "fundraising": {
            "priorita": "5x1000, micro-donazioni, bandi piccoli",
            "note": "Evitare fondazioni troppo grandi come Cariplo"
        }
    }
    return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
