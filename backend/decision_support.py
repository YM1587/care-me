from typing import Dict, List, Tuple
from feature_engineering import PatientData

URGENCY_CLASSES = {
    0: "Non-critical",
    1: "Critical"
}

def apply_clinical_rules(patient: PatientData, ml_prediction: int, ml_confidence: float) -> Tuple[int, List[str]]:
    """
    Applies strict clinical thresholds to override or validate the ML model's prediction.
    Ensures safe intelligence by escalating if critical limits are breached.
    
    Returns:
        Tuple of (Final Class Integer, List of Alert Strings)
    """
    alerts = []
    final_class = ml_prediction
    
    # 1. CRITICAL OVERRIDES (Hard Rules)
    # These vitals are universally concerning regardless of ML prediction.
    if patient.hr > 140:
        alerts.append("CRITICAL 🚨: Severe Tachycardia (HR > 140). Rule Override.")
        final_class = 1
    
    if patient.sbp < 80:
        alerts.append("CRITICAL 🚨: Severe Hypotension (SBP < 80). Rule Override.")
        final_class = 1
        
    if patient.spo2 is not None and patient.spo2 < 90:
        alerts.append("CRITICAL 🚨: Life-threatening Hypoxemia (SpO2 < 90%). Rule Override.")
        final_class = 1
        
    # 2. ADDITIONAL SAFETY CHECKS (Warning Zones)
    if patient.rr > 28:
        alerts.append("WARNING: Severe Tachypnea (RR > 28). Possible respiratory distress.")
        if final_class == 0:
            alerts.append("SAFETY ESCALATION: Vital signs suggest instability. Upgraded to Critical.")
            final_class = 1
            
    if patient.mental_state and patient.mental_state > 1:
        alerts.append(f"WARNING: Altered mental state (Code {patient.mental_state}).")
        if final_class == 0:
            final_class = 1 # Better safe than sorry for non-alert patients
            
    # 3. CONFIDENCE CHECK
    if ml_confidence < 0.60:
        alerts.append("⚠️ LOW AI CONFIDENCE: Manual assessment strongly advised.")
        # Borderline escalation logic
        if final_class == 0 and (patient.spo2 is not None and patient.spo2 < 94):
            alerts.append("SAFETY OVERRIDE: Low confidence + borderline SpO2. Escalated.")
            final_class = 1

    return final_class, alerts
