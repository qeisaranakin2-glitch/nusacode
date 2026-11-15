from flask import Flask, request, jsonify
from flask_cors import CORS
from compiler import compile_source

app = Flask(__name__)
CORS(app)

@app.get("/api/health")
def health():
    return jsonify({"status": "ok", "name": "NusaCode Compiler API"})

@app.post("/api/compile")
def compile_code():
    payload = request.get_json(silent=True) or {}
    source = payload.get("code", "")
    if not isinstance(source, str):
        return jsonify({"success": False, "error": "Field code harus berupa teks."}), 400
    if len(source) > 20000:
        return jsonify({"success": False, "error": "Kode terlalu panjang (maksimal 20.000 karakter)."}), 413
    result = compile_source(source)
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
