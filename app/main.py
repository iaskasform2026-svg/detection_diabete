from fastapi import Depends, FastAPI
from fastapi.responses import JSONResponse

from .auth import verify_token
from .model_service import ModelService
from .schemas import PatientFeatures, PredictionResponse

app = FastAPI(
    title="Medical Diabetes Risk API",
    version="1.0.0",
    description="API sécurisée de scoring du risque de diabète",
)
service = ModelService()


@app.get("/health")
def healthcheck() -> dict:
    return {"status": "ok", "model_version": service.version}


@app.post("/predict", response_model=PredictionResponse)
def predict(payload: PatientFeatures, _: str = Depends(verify_token)) -> PredictionResponse:
    result = service.predict(payload.model_dump())
    return PredictionResponse(**result)


@app.exception_handler(Exception)
async def generic_exception_handler(_, exc: Exception):
    return JSONResponse(status_code=500, content={"detail": str(exc)})
