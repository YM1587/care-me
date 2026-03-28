import joblib

model = joblib.load('triage_model_pipeline.joblib')
preprocessor = model.named_steps['preprocessor']
num_cols = preprocessor.transformers_[0][2]
cat_cols = preprocessor.transformers_[1][2]
print("Numerical (int/float) cols expected:")
print(num_cols)
print("Categorical (object/string) cols expected:")
print(cat_cols)
