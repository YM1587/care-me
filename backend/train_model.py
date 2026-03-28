import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib
import os

def generate_synthetic_data(n_samples=5000):
    np.random.seed(42)
    data = {
        'age': np.random.randint(18, 90, n_samples),
        'sex': np.random.choice([0, 1], n_samples), # 0: Female, 1: Male
        'sbp': np.random.normal(120, 20, n_samples).clip(60, 220), # Systolic BP
        'dbp': np.random.normal(80, 15, n_samples).clip(40, 130), # Diastolic BP
        'hr': np.random.normal(80, 20, n_samples).clip(40, 180), # Heart Rate
        'rr': np.random.normal(16, 4, n_samples).clip(8, 40), # Respiratory Rate
        'temp': np.random.normal(37.0, 1.0, n_samples).clip(34.0, 42.0), # Temperature
        'spo2': np.random.normal(98, 3, n_samples).clip(70, 100), # O2 Saturation
    }
    
    df = pd.DataFrame(data)
    
    # Derived features
    df['shock_index'] = df['hr'] / df['sbp']
    df['pulse_pressure'] = df['sbp'] - df['dbp']
    
    # Synthetic Labels based on thresholds (to simulate clinical reality)
    # 0: Non-Urgent, 1: Urgent, 2: Emergency
    conditions = [
        # Emergency: Shock, Severe Hypoxemia, Severe Tachycardia, Extreme Temp
        (df['sbp'] < 90) | (df['spo2'] < 92) | (df['hr'] > 130) | (df['rr'] > 28) | (df['temp'] > 40),
        
        # Urgent: Warning zones
        (df['sbp'] < 100) | (df['sbp'] > 180) | (df['spo2'] < 95) | (df['hr'] > 110) | (df['rr'] > 22) | (df['temp'] > 38.5)
    ]
    choices = [2, 1]
    df['urgency'] = np.select(conditions, choices, default=0)
    
    # Introduce some noise to make the ML model actually learn
    noise_mask = np.random.rand(n_samples) < 0.15
    df.loc[noise_mask, 'urgency'] = np.random.choice([0, 1, 2], size=noise_mask.sum())
    
    return df

def train_and_save_model():
    print("Generating synthetic triage data...")
    df = generate_synthetic_data(10000)
    
    X = df.drop(columns=['urgency'])
    y = df['urgency']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    print("Training Random Forest Classifier...")
    model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42, class_weight='balanced')
    model.fit(X_train, y_train)
    
    print("Evaluating model...")
    y_pred = model.predict(X_test)
    print(classification_report(y_test, y_pred, target_names=['Non-Urgent', 'Urgent', 'Emergency']))
    
    # Save the model
    os.makedirs(os.path.dirname(os.path.abspath(__file__)), exist_ok=True)
    model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'triage_rf_model.joblib')
    joblib.dump(model, model_path)
    print(f"Model saved to {model_path}")

if __name__ == "__main__":
    train_and_save_model()
