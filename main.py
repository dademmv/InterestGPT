from flask import Flask, jsonify, request
import os
import json

app = Flask(__name__)

# Percorso file JSON dove salvi i dati
DATA_FILE = "knowledge.json"

# Se esiste il file, carica i dati, altrimenti usa quelli base
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        knowledge = json.load(f)
else:
    knowledge = {
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

@app.route("/")
def home():
    return "Welcome to the Knowledge API! Visit /knowledge to get data."

@app.route("/knowledge", methods=["GET"])
def get_knowledge():
    return jsonify(knowledge)

@app.route("/knowledge/update", methods=["POST"])
def update_knowledge():
    content = request.json
    categoria = content.get("categoria")
    nuovo_valore = content.get("nuovo_valore")

    if categoria in knowledge:
        if isinstance(knowledge[categoria], list):
            knowledge[categoria].append(nuovo_valore)
        elif isinstance(knowledge[categoria], dict):
            knowledge[categoria].update(nuovo_valore)
        with open(DATA_FILE, "w") as f:
            json.dump(knowledge, f)
        return jsonify({"status": "ok", "updated": nuovo_valore})
    else:
        return jsonify({"error": "Categoria non valida"}), 400

@app.route("/knowledge/delete", methods=["DELETE"])
def delete_knowledge():
    content = request.json
    categoria = content.get("categoria")
    criterio = content.get("criterio")

    if categoria not in knowledge:
        return jsonify({"error": "Categoria non valida"}), 400

    if isinstance(knowledge[categoria], list):
        before = len(knowledge[categoria])
        knowledge[categoria] = [el for el in knowledge[categoria] if not all(el.get(k) == v for k, v in criterio.items())]
        after = len(knowledge[categoria])
        if before == after:
            return jsonify({"status": "niente da eliminare"}), 404
    elif isinstance(knowledge[categoria], dict):
        for k in list(criterio.keys()):
            knowledge[categoria].pop(k, None)

    with open(DATA_FILE, "w") as f:
        json.dump(knowledge, f)

    return jsonify({"status": "ok", "deleted": criterio})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
