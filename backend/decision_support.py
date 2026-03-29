from typing import Dict, List, Tuple
from feature_engineering import PatientData

URGENCY_CLASSES = {
    0: "Non-critical",
    1: "Critical"
}

def apply_clinical_rules(patient: PatientData, ml_prediction: int, ml_confidence: float, risk_prob: float) -> Tuple[str, List[str], Dict[str, str], int]:
    """
    Applies strict clinical thresholds and uses the Mistriage Risk Model (risk_prob)
    to determine the final clinical scenario.
    
    Returns:
        Tuple of (Final Recommendation String, List of Alert Strings, Dictionary of Rule Breaches, Scenario ID)
        Scenario IDs:
            1: Safe (Non-critical)
            2: Recheck (Non-critical ML + High Risk)
            3: Confirmed Critical (Critical ML + Low Risk)
            4: Complex Critical (Critical ML + High Risk)
    """
    alerts = []
    rule_breaches = {}
    is_critical_by_rules = False
    
    # 1. CRITICAL OVERRIDES (Hard Rules)
    if patient.hr > 140:
        rule_breaches["Heart Rate"] = f"{patient.hr} bpm (>140)"
        is_critical_by_rules = True
    
    if patient.sbp < 80:
        rule_breaches["Blood Pressure"] = f"{patient.sbp} mmHg (<80)"
        is_critical_by_rules = True
        
    if patient.spo2 is not None and patient.spo2 < 90:
        rule_breaches["Oxygen (SpO2)"] = f"{patient.spo2}% (<90%)"
        is_critical_by_rules = True

    if patient.rr > 30:
        rule_breaches["Resp Rate"] = f"{patient.rr} br/min (>30)"
        is_critical_by_rules = True

    if patient.mental_state and patient.mental_state > 1:
        rule_breaches["Mental State"] = f"Altered (Code {patient.mental_state})"
        is_critical_by_rules = True

    # 2. EVALUATING SCENARIO (Dual Model Logic)
    # ml_prediction: 0=Non-critical, 1=Critical
    # risk_prob: >0.5 is High Risk
    
    is_ml_critical = (ml_prediction == 1) or is_critical_by_rules
    # We use a slightly more sensitive threshold for the safety checker
    is_high_risk = (risk_prob > 0.40) 
    
    if is_ml_critical:
        if is_high_risk:
            scenario_id = 4 # Complex Critical
            recommendation = "Critical (High Complexity)"
            alerts.append("⚠️ HIGH COMPLEXITY: Patient is critical and exhibits unusual patterns. Senior review required.")
        else:
            scenario_id = 3 # Confirmed Critical
            recommendation = "Critical"
            alerts.append("✅ CONFIRMED CRITICAL: Immediate clinical intervention required.")
    else:
        if is_high_risk:
            scenario_id = 2 # Recheck Patient
            recommendation = "RECHECK PATIENT ⚠️"
            alerts.append("🚨 SAFETY ALERT: ML says non-critical, but Risk Model detected a high probability of mistriage. RE-EVALUATE MANUALLY.")
        else:
            scenario_id = 1 # Safe
            recommendation = "Non-critical"
            alerts.append("✔ SAFE STABLE: Patient vitals and AI assessment suggest non-urgent status.")

    return recommendation, alerts, rule_breaches, scenario_id
