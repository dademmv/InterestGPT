from flask import Flask, request, jsonify, send_from_directory
import os

app = Flask(__name__)

# Knowledge base in memoria
knowledge_base = {
    "progetti": [
        {
            "nome": "Finance for Schools",
            "partner": ["Starting Finance", "Italicamp"],
            "target": "Scuole secondarie",
            "note": "Seminari + contenuti digitali"
        }
    ],
    "governance": {
        "presidente": "Davide Franchini",
        "CTS": ["Marcella Panucci", "Matteo Petrella","Tommaso Pazienza","Antonio Cilento","Francesco Armillei"]
    },
    "fundraising": {
        "priorita": "5x1000, micro-donazioni, bandi piccoli",
        "note": "Evitare fondazioni troppo grandi"
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

    if isinstance(knowledge_base[categoria], dict):
        if not isinstance(nuovo_valore, dict):
            return jsonify({"errore": "Valore non valido per dizionario"}), 400
        knowledge_base[categoria].update(nuovo_valore)

    elif isinstance(knowledge_base[categoria], list):
        knowledge_base[categoria].append(nuovo_valore)
    else:
        return jsonify({"errore": "Tipo di categoria non gestita"}), 400

    return jsonify({"messaggio": "Knowledge aggiornata con successo"}), 200

# Endpoint per esporre i file del plugin
@app.route("/.well-known/ai-plugin.json")
def serve_ai_plugin():
    return send_from_directory('.', "ai-plugin.json", mimetype="application/json")

@app.route("/openapi.yaml")
def serve_openapi():
    return send_from_directory('.', "openapi.yaml", mimetype="text/yaml")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
