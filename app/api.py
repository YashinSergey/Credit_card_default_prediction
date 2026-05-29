import json
import logging
import os
import time

from flask import Flask, jsonify, request

try:
    from app.model_handler import MODEL_PATH, load_model, predict_default
except ModuleNotFoundError:
    from model_handler import MODEL_PATH, load_model, predict_default


app = Flask(__name__)
model_bundle = load_model(MODEL_PATH)
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)


def write_log(event, status_code, start_time, details=None):
    log_data = {
        "event": event,
        "status_code": status_code,
        "duration_ms": round((time.time() - start_time) * 1000, 2),
        "method": request.method,
        "path": request.path,
    }
    if details:
        log_data.update(details)

    logger.info(json.dumps(log_data, ensure_ascii=False))


@app.route("/health", methods=["GET"])
def health():
    start_time = time.time()
    write_log("health_check", 200, start_time)
    return jsonify({"status": "healthy"}), 200


@app.route("/predict", methods=["POST"])
def predict():
    start_time = time.time()

    try:
        data = request.get_json()
        if not isinstance(data, dict):
            write_log("predict_error", 400, start_time, {"error": "invalid_json"})
            return jsonify({"error": "Request body must be a JSON object"}), 400

        result = predict_default(data, model_bundle)
        write_log(
            "predict_success",
            200,
            start_time,
            {
                "prediction": result["prediction"],
                "probability": round(result["probability"], 4),
                "model_version": result["model_version"],
            },
        )
        return jsonify(result), 200
    except Exception as error:
        write_log("predict_error", 400, start_time, {"error": str(error)})
        return jsonify({"error": str(error)}), 400


if __name__ == "__main__":
    host = os.getenv("FLASK_HOST", "127.0.0.1")
    port = int(os.getenv("PORT", "5001"))

    app.run(host=host, port=port, debug=False)
