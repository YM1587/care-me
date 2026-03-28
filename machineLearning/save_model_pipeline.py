import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from imblearn.over_sampling import SMOTE
import joblib

print("Loading data...")
df1 = pd.read_csv("data.csv", encoding='latin1', sep=';', engine='python', on_bad_lines='skip')

target = 'KTAS_expert'
leakage_cols = ['Diagnosis in ED', 'Disposition', 'Error_group', 'Length of stay_min', 
                'KTAS duration_min', 'mistriage', 'KTAS_RN', 'Group', 'Patients number per hour']

df_care = df1.drop(columns=[col for col in leakage_cols if col in df1.columns]).copy()
df_care = df_care.dropna(subset=[target])

# Fix formatting of vital signs that pandas treated as strings due to commas
vitals = ['SBP', 'DBP', 'HR', 'RR', 'BT', 'Saturation', 'NRS_pain']
for v in vitals:
    if v in df_care.columns:
        df_care[v] = df_care[v].astype(str).str.replace(',', '.')
        df_care[v] = pd.to_numeric(df_care[v], errors='coerce')

y = df_care[target].astype(int)
X = df_care.drop(columns=[target])

categorical_cols = X.select_dtypes(include=['object']).columns.tolist()
numerical_cols = X.select_dtypes(exclude=['object']).columns.tolist()

print("Numerical cols:", numerical_cols)
print("Categorical cols:", categorical_cols)

numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])

categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])

preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numerical_cols),
        ('cat', categorical_transformer, categorical_cols)
    ])

print("Splitting and pre-processing data...")
# We use Pipeline to bundle preprocessor and modeling step. 
# BUT wait! SMOTE needs to be applied to the preprocessed training set, but NOT the validation set.
# A standard sklearn Pipeline doesn't support SMOTE inside it (we would need imblearn.pipeline.Pipeline).
# So let's build an imblearn pipeline.
from imblearn.pipeline import Pipeline as ImbPipeline

model_pipeline = ImbPipeline(steps=[
    ('preprocessor', preprocessor),
    ('smote', SMOTE(random_state=42)),
    ('classifier', RandomForestClassifier(n_estimators=200, random_state=42, class_weight='balanced'))
])

print("Training model pipeline...")
model_pipeline.fit(X, y)

print("Saving model pipeline...")
joblib.dump(model_pipeline, 'triage_model_pipeline.joblib')

print("Model successfully saved as 'triage_model_pipeline.joblib'")
