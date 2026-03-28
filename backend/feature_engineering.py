from pydantic import BaseModel, conint, confloat, Field
from typing import Optional

class PatientData(BaseModel):
    # Demographics
    age: conint(ge=0, le=120)
    sex: str # "Male" or "Female"
    arrival_mode: conint(ge=1, le=7) # typically 1=walk-in, 3=ambulance etc
    injury: conint(ge=1, le=2) # 1=No, 2=Yes
    
    # Clinical presentation
    chief_complain: str
    mental_state: conint(ge=1, le=4) # 1=alert, 2=verbal, 3=pain, 4=unresponsive
    pain: conint(ge=0, le=1) # 0=No, 1=Yes
    nrs_pain: confloat(ge=0, le=10) # 0-10 pain scale
    
    # Vitals
    sbp: confloat(ge=0) # Systolic Blood Pressure
    dbp: confloat(ge=0) # Diastolic Blood Pressure
    hr: confloat(ge=0) # Heart Rate
    rr: confloat(ge=0) # Respiratory Rate
    temp: confloat(ge=0) # Temperature in Celsius
    spo2: confloat(ge=0, le=100) # Oxygen saturation

def engineer_features(patient: PatientData) -> dict:
    """Converts raw patient data into the numerical format expected by the model."""
    sex_num = 1 if patient.sex.lower() == "male" else 2
    
    return {
        "Sex": sex_num,
        "Age": patient.age,
        "Arrival mode": patient.arrival_mode,
        "Injury": patient.injury,
        "Chief_complain": patient.chief_complain,
        "Mental": patient.mental_state,
        "Pain": patient.pain,
        "NRS_pain": patient.nrs_pain,
        "SBP": patient.sbp,
        "DBP": patient.dbp,
        "HR": patient.hr,
        "RR": patient.rr,
        "BT": patient.temp,
        "Saturation": patient.spo2
    }
