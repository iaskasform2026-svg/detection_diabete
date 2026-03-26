from __future__ import annotations

from pathlib import Path
from typing import Any
import os
import joblib
import pandas as pd

MODEL_PATH = Path(os.getenv("MODEL_PATH", "models/diabetes_risk_model.joblib"))
MODEL_VERSION = os.getenv("MODEL_VERSION", "1.0.0")
DEFAULT_THRESHOLD = float(os.getenv("PREDICTION_THRESHOLD", "0.50"))


class FallbackModel:
    """Used when no serialized model is available yet."""

    def predict_proba(self, X: pd.DataFrame):
        # Heuristic fallback only for technical demo purposes.
        score = (
            (X["glucose_level"] / 200).clip(0, 1) * 0.35
            + (X["hba1c"] / 10).clip(0, 1) * 0.30
            + (X["bmi"] / 50).clip(0, 1) * 0.15
            + (X["retinopathy_score"]).clip(0, 1) * 0.10
            + (X["family_history"] * 0.05)
            + (X["smoker"] * 0.05)
        )
        score = score.clip(0, 1)
        return pd.DataFrame({0: 1 - score, 1: score}).values


class ModelService:
    def __init__(self) -> None:
        self.model = self._load_model()
        self.version = MODEL_VERSION
        self.threshold = DEFAULT_THRESHOLD

    def _load_model(self) -> Any:
        if MODEL_PATH.exists():
            return joblib.load(MODEL_PATH)
        return FallbackModel()

    def predict(self, payload: dict) -> dict:
        X = pd.DataFrame([payload])
        proba = float(self.model.predict_proba(X)[:, 1][0])
        predicted_class = int(proba >= self.threshold)
        return {
            "risk_score": round(proba, 4),
            "predicted_class": predicted_class,
            "model_version": self.version,
            "threshold": self.threshold,
            "message": "Risque eleve" if predicted_class == 1 else "Risque faible a modere",
        }
