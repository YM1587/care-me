from pydantic import BaseModel, conint, confloat
from typing import Optional

class PatientData(BaseModel):
    # Demographics
    age: Optional[conint(ge=0, le=120)] = None # Numeric age (if known)
    age_group: Optional[conint(ge=0, le=3)] = None # 0=0-18, 1=19-40, 2=41-65, 3=66+
    sex: str # "Male" or "Female"
    arrival_mode: conint(ge=1, le=7)
    injury: conint(ge=1, le=2)
    
    # Clinical presentation
    chief_complain: Optional[str] = "None"
    mental_state: conint(ge=1, le=4)
    pain: conint(ge=0, le=1)
    nrs_pain: confloat(ge=0, le=10)
    
    # Vitals
    sbp: confloat(ge=0)
    dbp: confloat(ge=0)
    hr: confloat(ge=0)
    rr: confloat(ge=0)
    temp: confloat(ge=0)
    spo2: Optional[confloat(ge=0, le=100)] = None

def get_age_group(age: int) -> int:
    """Fallback logic if direct age_group isn't provided from frontend."""
    if age <= 18: return 0
    elif age <= 40: return 1
    elif age <= 65: return 2
    else: return 3

def engineer_features(patient: PatientData) -> dict:
    """Converts raw patient data into the numerical format expected by the model."""
    
    # 1. Sex encoding (1=Female, 2=Male)
    sex_num = 2 if patient.sex.lower() == "male" else 1
    
    # 2. Saturation handling
    sat_missing = 1 if patient.spo2 is None else 0
    saturation = patient.spo2 if patient.spo2 is not None else 98.0
    
    # 3. Derived Vitals
    # CRITICAL: Case must match training exactly (Shock_Index)
    shock_index = patient.hr / patient.sbp if patient.sbp != 0 else 0
    pulse_pressure = patient.sbp - patient.dbp
    
    # 4. Age and Age Group
    # Use direct group if provided (unconscious patient), else derive from age
    age_group = patient.age_group if patient.age_group is not None else get_age_group(patient.age or 45)
    age_val = patient.age if patient.age is not None else [9, 30, 52, 75][age_group]
    
    return {
        "Group": 1, # System Default
        "Sex": sex_num,
        "Age": age_val,
        "Patients number per hour": 5, # System Default
        "Arrival mode": patient.arrival_mode,
        "Injury": patient.injury,
        "Chief_complain": patient.chief_complain or "None",
        "Mental": patient.mental_state,
        "Pain": patient.pain,
        "NRS_pain": patient.nrs_pain,
        "SBP": patient.sbp,
        "DBP": patient.dbp,
        "HR": patient.hr,
        "RR": patient.rr,
        "BT": patient.temp,
        "Saturation": saturation,
        "KTAS duration_min": 0, # System Default
        "Saturation_missing": sat_missing,
        "Shock_Index": shock_index,
        "Pulse_Pressure": pulse_pressure,
        "Age_group": age_group
    }
