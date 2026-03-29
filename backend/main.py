from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import joblib
import pandas as pd
import os
import numpy as np

# Use local module imports
from feature_engineering import PatientData, engineer_features
from decision_support import apply_clinical_rules

app = FastAPI(title="CareMe AI-Powered Triage API")

# Setup CORS for the React Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Paths for the new independent models (Pipelines)
URGENCY_MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "models", "urgency_model_xgb.pkl")
RISK_MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "models", "mistriage_risk_model_rf.pkl")

# Load ML Models
urgency_model = None
risk_model = None

if os.path.exists(URGENCY_MODEL_PATH):
    urgency_model = joblib.load(URGENCY_MODEL_PATH)
    print("Urgency model loaded successfully.")
else:
    print(f"Warning: Urgency model not found at {URGENCY_MODEL_PATH}.")

if os.path.exists(RISK_MODEL_PATH):
    risk_model = joblib.load(RISK_MODEL_PATH)
    print("Risk (Mistriage) model loaded successfully.")
else:
    print(f"Warning: Risk model not found at {RISK_MODEL_PATH}.")

@app.post("/api/predict")
async def predict_triage(patient: PatientData):
    if urgency_model is None:
        raise HTTPException(status_code=500, detail="Urgency model is unavailable.")
    
    # 1. Feature Engineering
    features = engineer_features(patient)
    df = pd.DataFrame([features])
    
    # 2. Urgency Prediction
    try:
        predicted_class_int = int(urgency_model.predict(df)[0])
        probabilities = urgency_model.predict_proba(df)[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error (Urgency): {str(e)}")
    
    ml_confidence = float(np.max(probabilities))
    ml_prediction_class = "Critical" if predicted_class_int == 1 else "Non-critical"
    
    # 3. Risk (Mistriage) Prediction
    risk_prob = 0.0
    if risk_model is not None:
        try:
            # The Risk Model expects 20 features (drops Chief_complain)
            risk_df = df.drop(columns=["Chief_complain"]) if "Chief_complain" in df.columns else df
            risk_probs = risk_model.predict_proba(risk_df)[0]
            # If the risk model was binary 0/1, index 1 is the positive outcome
            risk_prob = float(risk_probs[1]) if len(risk_probs) > 1 else float(risk_probs[0])
        except Exception as e:
            print(f"Risk prediction failed: {e}")
    
    # 4. Decision Support Layer (SATS/KTAS Standardized Logic)
    recommendation, alerts, breaches, scenario_id, warnings = apply_clinical_rules(
        patient, predicted_class_int, ml_confidence, risk_prob
    )
    
    # 5. SEGREGATED RESPONSE (Explainability segments)
    response = {
        "ai_insights": {
            "prediction": ml_prediction_class,
            "confidence": ml_confidence,
            "mistriage_risk": risk_prob,
            "risk_label": "High" if risk_prob > 0.45 else "Low",
            "probabilities": {
                "Non-critical": float(probabilities[0]),
                "Critical": float(probabilities[1])
            }
        },
        "clinical_protocol": {
            "final_recommendation": recommendation,
            "scenario_id": scenario_id,
            "rule_breaches": breaches, # Critical (Red)
            "rule_warnings": warnings, # Urgent (Orange/Yellow)
            "alerts": alerts
        }
    }
    
    return response

@app.get("/api/status")
async def status():
    return {
        "status": "ok", 
        "urgency_model_loaded": urgency_model is not None,
        "risk_model_loaded": risk_model is not None
    }
