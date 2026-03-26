
from pathlib import Path
import joblib
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel

MODEL_PATH = Path("outputs/best_diabetes_risk_model.joblib")
app = FastAPI(title="Diabetes Risk API", version="1.0.0")

model = joblib.load(MODEL_PATH)

class PatientInput(BaseModel):
    age: float
    gender: str
    bmi: float
    glucose_level: float
    hba1c: float
    blood_pressure: float
    cholesterol: float
    triglycerides: float
    retinopathy_score: float
    family_history: int
    physical_activity_level: str
    smoker: int

def enrich_features(payload: dict) -> pd.DataFrame:
    df = pd.DataFrame([payload])
    df["is_hypertensive_proxy"] = (df["blood_pressure"] >= 140).astype(int)
    df["is_obese_proxy"] = (df["bmi"] >= 30).astype(int)
    df["is_hyperglycemic_proxy"] = (df["glucose_level"] >= 140).astype(int)
    df["is_high_hba1c_proxy"] = (df["hba1c"] >= 6.5).astype(int)
    df["is_dyslipidemic_proxy"] = (
        (df["cholesterol"] >= 200) | (df["triglycerides"] >= 150)
    ).astype(int)

    def bmi_category(bmi):
        if bmi < 18.5:
            return "insuffisance_ponderale"
        elif bmi < 25:
            return "normal"
        elif bmi < 30:
            return "surpoids"
        return "obesite"

    df["bmi_category"] = df["bmi"].apply(bmi_category)
    df["cardio_metabolic_burden"] = df[
        [
            "is_hypertensive_proxy",
            "is_obese_proxy",
            "is_hyperglycemic_proxy",
            "is_high_hba1c_proxy",
            "is_dyslipidemic_proxy",
            "family_history",
            "smoker",
        ]
    ].sum(axis=1)
    return df

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict")
def predict(patient: PatientInput):
    df = enrich_features(patient.model_dump())
    proba = float(model.predict_proba(df)[0, 1])
    pred = int(model.predict(df)[0])
    return {
        "diabetes_risk_prediction": pred,
        "diabetes_risk_probability": round(proba, 4),
        "warning": "Aide à la décision uniquement. Validation médicale obligatoire."
    }
