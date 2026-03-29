from typing import Dict, List, Tuple
from feature_engineering import PatientData

def apply_clinical_rules(patient: PatientData, ml_prediction: int, ml_confidence: float, risk_prob: float) -> Tuple[str, List[str], Dict[str, str], int, Dict[str, str]]:
    """
    Applies strict clinical thresholds (SATS/KTAS) and uses the Mistriage Risk Model
    to determine the final clinical scenario and recommendation.
    
    Returns:
        Tuple of (
            Final Recommendation, 
            Alerts, 
            Rule Breaches (Critical), 
            Scenario ID, 
            Clinical Warnings (Urgent)
        )
    """
    alerts = []
    rule_breaches = {} # Critical (Red)
    clinical_warnings = {} # Urgent (Orange/Yellow)
    
    # 1. Derived Indicators
    shock_index = patient.hr / patient.sbp if patient.sbp != 0 else 0
    pulse_pressure = patient.sbp - patient.dbp
    
    # 2. EVALUATE THRESHOLDS (Clinically Grounded)
    
    # Heart Rate
    if patient.hr > 130 or patient.hr < 40:
        rule_breaches["Heart Rate"] = f"{patient.hr} bpm (Severe)"
    elif (100 <= patient.hr <= 130) or (40 <= patient.hr <= 50):
        clinical_warnings["Heart Rate"] = f"{patient.hr} bpm (Abnormal)"
        
    # Blood Pressure (Systolic)
    if patient.sbp < 90 or patient.sbp > 180:
        rule_breaches["Blood Pressure"] = f"{patient.sbp} mmHg (Critical)"
    elif 90 <= patient.sbp <= 100:
        clinical_warnings["Blood Pressure"] = f"{patient.sbp} mmHg (Borderline)"
        
    # Respiratory Rate
    if patient.rr > 30 or patient.rr < 8:
        rule_breaches["Resp Rate"] = f"{patient.rr} br/min (Distress)"
    elif 20 <= patient.rr <= 30 or 8 <= patient.rr <= 12:
        clinical_warnings["Resp Rate"] = f"{patient.rr} br/min (Elevated)"
        
    # Oxygen Saturation
    if patient.spo2 is not None:
        if patient.spo2 < 90:
            rule_breaches["Oxygen (SpO2)"] = f"{patient.spo2}% (Severe Hypoxia)"
        elif 90 <= patient.spo2 <= 94:
            clinical_warnings["Oxygen (SpO2)"] = f"{patient.spo2}% (Low)"
            
    # Temperature
    if patient.temp > 39 or patient.temp < 35:
        rule_breaches["Temperature"] = f"{patient.temp}°C (Critical)"
    elif 38 <= patient.temp <= 39:
        clinical_warnings["Temperature"] = f"{patient.temp}°C (Fever)"
        
    # Mental Status
    if patient.mental_state >= 3:
        rule_breaches["Mental Status"] = f"Code {patient.mental_state} (Severe)"
    elif patient.mental_state == 2:
        clinical_warnings["Mental Status"] = f"Code 2 (Altered)"
        
    # Shock Index
    if shock_index > 1.0:
        rule_breaches["Shock Index"] = f"{shock_index:.2f} (Shock Likely)"
    elif 0.7 <= shock_index <= 1.0:
        clinical_warnings["Shock Index"] = f"{shock_index:.2f} (Concerning)"
        
    # Pulse Pressure
    if pulse_pressure < 20:
        rule_breaches["Pulse Pressure"] = f"{pulse_pressure} mmHg (Narrow)"
    elif pulse_pressure > 60:
        clinical_warnings["Pulse Pressure"] = f"{pulse_pressure} mmHg (Wide)"

    # 3. FINAL DECISION LOGIC (The "Brain" Integration)
    is_critical_override = len(rule_breaches) > 0
    is_urgent_override = len(clinical_warnings) > 0
    
    # ml_prediction: 0=Non-critical, 1=Critical
    # risk_prob: >0.45 is High Risk
    is_ml_critical = (ml_prediction == 1)
    is_high_risk = (risk_prob > 0.45)
    
    # SCENARIO DETERMINATION
    if is_critical_override:
        scenario_id = 3 # Confirmed Critical (Override)
        recommendation = "Critical (Safety Override - Vital Signs)"
        alerts.append("CRITICAL: Patient vitals indicate immediate life threat. Standard Protocols: Level 1 (Resuscitation).")
    
    elif is_ml_critical:
        if is_high_risk:
            scenario_id = 4 # Complex Critical
            recommendation = "Critical (High AI Risk - Review Immediately)"
            alerts.append("URGENT: ML flags critical status with high uncertainty. Comprehensive diagnostic review required.")
        else:
            scenario_id = 3 # Confirmed Critical
            recommendation = "Critical (AI Recommendation)"
            alerts.append("URGENT: AI predicts high acuity. Move to stabilization area.")
            
    elif is_high_risk or is_urgent_override:
        scenario_id = 2 # Re-evaluate
        recommendation = "Re-evaluate Patient (Safety Alert)"
        alerts.append("WARNING: AI predicts stability but Clinical Rules or Risk Model flag potential mistriage. Reassess vitals manually.")
        
    else:
        scenario_id = 1 # Safe
        recommendation = "Non-critical (Care Plan Validated)"
        alerts.append("STABLE: Patient currently stable. Routine monitoring and standard care protocol initiated.")

    return recommendation, alerts, rule_breaches, scenario_id, clinical_warnings
