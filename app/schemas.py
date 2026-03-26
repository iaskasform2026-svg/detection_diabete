from pydantic import BaseModel, Field


class PatientFeatures(BaseModel):
    age: int = Field(..., ge=0, le=120)
    gender: str = Field(..., examples=["F", "M"])
    bmi: float = Field(..., ge=0)
    glucose_level: float = Field(..., ge=0)
    hba1c: float = Field(..., ge=0)
    blood_pressure: float = Field(..., ge=0)
    cholesterol: float = Field(..., ge=0)
    triglycerides: float = Field(..., ge=0)
    retinopathy_score: float = Field(..., ge=0)
    family_history: int = Field(..., ge=0, le=1)
    physical_activity_level: str = Field(..., examples=["faible", "moderee", "elevee"])
    smoker: int = Field(..., ge=0, le=1)


class PredictionResponse(BaseModel):
    risk_score: float
    predicted_class: int
    model_version: str
    threshold: float
    message: str
