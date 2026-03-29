import joblib
import pandas as pd

def inspect_model(name, path):
    print(f"\n--- {name} ---")
    try:
        model = joblib.load(path)
        if hasattr(model, 'feature_names_in_'):
            features = list(model.feature_names_in_)
            print(f"Features ({len(features)}):")
            print(", ".join(features))
        else:
            print("No feature_names_in_ attribute.")
    except Exception as e:
        print(f"Error: {e}")

inspect_model("Urgency Model", "models/urgency_model_xgb.pkl")
inspect_model("Risk Model", "models/mistriage_risk_model_rf.pkl")
