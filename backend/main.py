from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import joblib
import pandas as pd
import os
import numpy as np

# Use absolute imports or local module imports based on how it runs
from feature_engineering import PatientData, engineer_features
from decision_support import apply_clinical_rules, URGENCY_CLASSES

app = FastAPI(title="AI-Powered Patient Triage Support API")

# Setup CORS for the React Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Since it's a local test build
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MODEL_PATH = os.path.join(os.path.dirname(__file__), "triage_model_pipeline.joblib")

# Load ML Model
rf_model = None
if os.path.exists(MODEL_PATH):
    rf_model = joblib.load(MODEL_PATH)
    print("Pre-trained Random Forest Pipeline loaded successfully.")
else:
    print(f"Warning: Model not found at {MODEL_PATH}.")

@app.post("/api/predict")
async def predict_triage(patient: PatientData):
    if rf_model is None:
        raise HTTPException(status_code=500, detail="Model is currently unavailable. Please train it first.")
    
    # Feature Engineering
    features = engineer_features(patient)
    df = pd.DataFrame([features])
    
    # Predict using the random forest model
    predicted_class_int = int(rf_model.predict(df)[0])
    probabilities = rf_model.predict_proba(df)[0]
    
    # AI Output
    ml_confidence = float(np.max(probabilities))
    ml_prediction_class = URGENCY_CLASSES[predicted_class_int]
    
    # Decision Support Logic
    final_class_int, alerts = apply_clinical_rules(patient, predicted_class_int, ml_confidence)
    final_class = URGENCY_CLASSES[final_class_int]
    
    # Feature importance retrieval (mocked for simplicity, could extract real if requested)
    # The Random Forest provides actual importance across the dataset, but not individual SHAP explicitly here.
    # Instead, we just pass the most important raw features back.
    critical_features = []
    if final_class_int == 2:
        if patient.spo2 < 92: critical_features.append({"name": "SpO2", "value": f"{patient.spo2}%", "risk": "High"})
        if patient.sbp < 90: critical_features.append({"name": "Systolic BP", "value": patient.sbp, "risk": "High"})
        if patient.hr > 130: critical_features.append({"name": "Heart Rate", "value": patient.hr, "risk": "High"})

    response = {
        "original_ml_prediction": ml_prediction_class,
        "final_recommendation": final_class,
        "confidence_score": ml_confidence,
        "probabilities": {
            "Non-Urgent": float(probabilities[0]),
            "Urgent": float(probabilities[1]),
            "Emergency": float(probabilities[2])
        },
        "overridden_by_rules": final_class_int != predicted_class_int,
        "alerts": alerts,
        "influential_features": critical_features
    }
    
    return response

@app.get("/api/status")
async def status():
    return {"status": "ok", "model_loaded": rf_model is not None}
