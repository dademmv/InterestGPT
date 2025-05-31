from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Knowledge base in memoria (può essere poi caricata/salvata da JSON o DB)
knowledge_base = {
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
    return jsonify(knowledge_base)

@app.route("/knowledge/update", methods=["POST"])
def update_knowledge():
    content = request.json
    categoria = content.get("categoria")
    nuovo_valore = content.get("nuovo_valore")

    if categoria not in knowledge_base:
        return jsonify({"errore": "Categoria non valida"}), 400

    # Se categoria è un dizionario (es. governance o fundraising)
    if isinstance(knowledge_base[categoria], dict):
        if not isinstance(nuovo_valore, dict):
            return jsonify({"errore": "Valore non valido per dizionario"}), 400
        knowledge_base[categoria].update(nuovo_valore)
    # Se categoria è una lista (es. progetti)
    elif isinstance(knowledge_base[categoria], list):
        knowledge_base[categoria].append(nuovo_valore)
    else:
        return jsonify({"errore": "Tipo di categoria non gestita"}), 400

    return jsonify({"messaggio": "Knowledge aggiornata con successo"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
