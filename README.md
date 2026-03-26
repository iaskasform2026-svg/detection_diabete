# Modules d'industrialisation — IA médicale diabète

## Contenu
- `app/` : API sécurisée FastAPI
- `scripts/train.py` : entraînement et sérialisation du modèle
- `monitoring/monitor.py` : suivi simple des dérives et évolution des distributions
- `Dockerfile` : conteneurisation
- `.github/workflows/ci-cd.yml` : pipeline CI/CD

## Lancer localement
```bash
python scripts/train.py
uvicorn app.main:app --reload
```

## Exemple d'appel API
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Authorization: Bearer change-me-in-production" \
  -H "Content-Type: application/json" \
  -d '{
    "age": 57,
    "gender": "F",
    "bmi": 31.2,
    "glucose_level": 145,
    "hba1c": 6.8,
    "blood_pressure": 138,
    "cholesterol": 212,
    "triglycerides": 195,
    "retinopathy_score": 0.62,
    "family_history": 1,
    "physical_activity_level": "faible",
    "smoker": 0
  }'
```
