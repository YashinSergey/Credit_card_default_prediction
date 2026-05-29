import os

from flask import Flask, jsonify, request

try:
    from app.model_handler import MODEL_PATH, load_model, predict_default
except ModuleNotFoundError:
    from model_handler import MODEL_PATH, load_model, predict_default


app = Flask(__name__)
model_bundle = load_model(MODEL_PATH)


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy"}), 200


@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        if not isinstance(data, dict):
            return jsonify({"error": "Request body must be a JSON object"}), 400

        result = predict_default(data, model_bundle)
        return jsonify(result), 200
    except Exception as error:
        return jsonify({"error": str(error)}), 400


if __name__ == "__main__":
    host = os.getenv("FLASK_HOST", "127.0.0.1")
    port = int(os.getenv("PORT", "5001"))

    app.run(host=host, port=port, debug=False)
