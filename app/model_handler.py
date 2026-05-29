from pathlib import Path

import joblib
import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
MODEL_PATH = BASE_DIR / "models" / "logistic_regression_model.joblib"
MODEL_VERSION = "logistic_regression_v1"


def load_model(path=MODEL_PATH):
    return joblib.load(path)


def predict_default(client_data, model_bundle):
    client_df = pd.DataFrame([client_data])

    # Признаки должны идти в том же порядке, что и при обучении
    features = model_bundle["features"]
    missing_features = [feature for feature in features if feature not in client_df.columns]
    if missing_features:
        raise ValueError(f"Missing features: {missing_features}")

    client_df = client_df[features]
    probability = model_bundle["model"].predict_proba(client_df)[0][1]
    prediction = int(probability >= model_bundle["threshold"])

    return {
        "prediction": prediction,
        "probability": float(probability),
        "threshold": float(model_bundle["threshold"]),
        "model_version": MODEL_VERSION,
    }
