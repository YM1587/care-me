from pydantic import BaseModel, conint, confloat
from typing import Optional

class PatientData(BaseModel):
    age: conint(ge=0, le=120)
    sex: str # "Male" or "Female"
    sbp: confloat(ge=0) # Systolic Blood Pressure
    dbp: confloat(ge=0) # Diastolic Blood Pressure
    hr: confloat(ge=0) # Heart Rate
    rr: confloat(ge=0) # Respiratory Rate
    temp: confloat(ge=0) # Temperature in Celsius
    spo2: confloat(ge=0, le=100) # Oxygen saturation
    
    # Context (optional, could be used by rules)
    complaint: Optional[str] = "None"
    mental_state: Optional[str] = "Alert"

def engineer_features(patient: PatientData) -> dict:
    """Converts raw patient data into the numerical format expected by the model."""
    sex_num = 1 if patient.sex.lower() == "male" else 0
    shock_index = patient.hr / patient.sbp if patient.sbp > 0 else 0
    pulse_pressure = patient.sbp - patient.dbp
    
    return {
        "age": patient.age,
        "sex": sex_num,
        "sbp": patient.sbp,
        "dbp": patient.dbp,
        "hr": patient.hr,
        "rr": patient.rr,
        "temp": patient.temp,
        "spo2": patient.spo2,
        "shock_index": shock_index,
        "pulse_pressure": pulse_pressure
    }
