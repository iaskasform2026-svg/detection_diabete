FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY models ./models

ENV API_TOKEN=change-me-in-production
ENV MODEL_PATH=/app/models/diabetes_risk_model.joblib
ENV MODEL_VERSION=1.0.0
ENV PREDICTION_THRESHOLD=0.50

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
