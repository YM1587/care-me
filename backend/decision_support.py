from typing import Dict, List, Tuple
from .feature_engineering import PatientData

URGENCY_CLASSES = {
    0: "Non-Urgent",
    1: "Urgent",
    2: "Emergency"
}

def apply_clinical_rules(patient: PatientData, ml_prediction: int, ml_confidence: float) -> Tuple[int, List[str]]:
    """
    Applies strict clinical thresholds to override or validate the ML model's prediction.
    Ensures safe intelligence by escalating if critical limits are breached,
    or flagging high uncertainty.
    
    Returns:
        Tuple of (Final Urgency Class Integer, List of Alert Strings)
    """
    alerts = []
    final_class = ml_prediction
    
    # 1. Extreme Critical Thresholds (Always Emergency)
    if patient.spo2 < 92:
        alerts.append("CRITICAL: Severe hypoxemia (SpO2 < 92%). Escalated to Emergency.")
        final_class = 2
    
    if patient.sbp < 90:
        alerts.append("CRITICAL: Hypotension (SBP < 90). Risk of Shock. Escalated to Emergency.")
        final_class = 2
        
    if patient.hr > 130:
        alerts.append("CRITICAL: Severe Tachycardia (HR > 130). Escalated to Emergency.")
        final_class = 2
        
    if patient.rr > 28:
        alerts.append("CRITICAL: Severe Tachypnea (RR > 28). Respiratory distress risk. Escalated to Emergency.")
        final_class = 2
        
    if patient.mental_state and patient.mental_state.lower() != "alert":
        alerts.append(f"WARNING: Altered mental state recognized ({patient.mental_state}). Check airway.")
        if final_class < 1:
             final_class = 1 # At least Urgent
    
    # 2. Confidence Checks
    if ml_confidence < 0.60:
        alerts.append("WARNING: AI model confidence is low. Manual clinical review strongly advised.")
        # If low confidence and model said non-urgent, bump to urgent for safety if any borderline vitals
        if final_class == 0 and (patient.spo2 < 95 or patient.hr > 100):
             alerts.append("SAFETY OVERRIDE: Low confidence + borderline vitals. Escalated to Urgent.")
             final_class = 1

    # 3. Prevent ML Model from downgrading a rule-based Emergency
    if ml_prediction == 0 and final_class == 2:
        alerts.append("MISCLASSIFICATION ALERT: Model suggested Non-Urgent, but patient meets critical emergency criteria.")
        
    return final_class, alerts
