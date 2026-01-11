# app.py
from flask import Flask, request, jsonify
import json
from api.handler import handler

app = Flask(__name__)

@app.route("/rag", methods=["POST"])
def rag():
    data = request.get_json()
    result = handler({"query": data.get("query", "")})
    return jsonify(json.loads(result["body"]))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
