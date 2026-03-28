from pydantic import BaseModel, conint, confloat
from typing import Optional

class PatientData(BaseModel):
    # Demographics
    age: conint(ge=0, le=120)
    sex: str # "Male" or "Female"
    arrival_mode: conint(ge=1, le=7) # 1=walk-in, 3=ambulance etc
    injury: conint(ge=1, le=2) # 1=No, 2=Yes
    
    # Clinical presentation
    mental_state: conint(ge=1, le=4) # 1=alert, 2=verbal, 3=pain, 4=unresponsive
    pain: conint(ge=0, le=1) # 0=No, 1=Yes
    nrs_pain: confloat(ge=0, le=10) # 0-10 pain scale
    
    # Vitals
    sbp: confloat(ge=0) # Systolic Blood Pressure
    dbp: confloat(ge=0) # Diastolic Blood Pressure
    hr: confloat(ge=0) # Heart Rate
    rr: confloat(ge=0) # Respiratory Rate
    temp: confloat(ge=0) # Temperature in Celsius
    spo2: Optional[confloat(ge=0, le=100)] = None # Oxygen saturation

def get_age_group(age: int) -> int:
    """Exactly matches the training bins: [0, 18, 40, 65, 120] -> [0, 1, 2, 3]"""
    if age <= 18:
        return 0
    elif age <= 40:
        return 1
    elif age <= 65:
        return 2
    else:
        return 3

def engineer_features(patient: PatientData) -> dict:
    """Converts raw patient data into the numerical format expected by the model."""
    
    # 1. Sex encoding (1=Female, 2=Male)
    sex_num = 2 if patient.sex.lower() == "male" else 1
    
    # 2. Saturation handling
    sat_missing = 1 if patient.spo2 is None else 0
    saturation = patient.spo2 if patient.spo2 is not None else 98.0 # Median-ish value
    
    # 3. Derived Vitals
    shock_index = patient.hr / patient.sbp if patient.sbp != 0 else 0
    pulse_pressure = patient.sbp - patient.dbp
    
    # 4. Age Group
    age_group = get_age_group(patient.age)
    
    # 5. System Defaults (as per latest training report)
    patients_per_hour = 5
    hospital_group = 1
    ktas_duration = 0
    
    return {
        "Age": patient.age,
        "Sex": sex_num,
        "Age_group": age_group,
        "Arrival mode": patient.arrival_mode,
        "Injury": patient.injury,
        "Patients number per hour": patients_per_hour,
        "Group": hospital_group,
        "Mental": patient.mental_state,
        "Pain": patient.pain,
        "NRS_pain": patient.nrs_pain,
        "SBP": patient.sbp,
        "DBP": patient.dbp,
        "HR": patient.hr,
        "RR": patient.rr,
        "BT": patient.temp,
        "Saturation": saturation,
        "Shock_index": shock_index,
        "Pulse_Pressure": pulse_pressure,
        "Saturation_missing": sat_missing,
        "KTAS duration_min": ktas_duration
    }
