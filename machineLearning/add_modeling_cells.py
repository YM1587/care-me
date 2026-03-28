import json

with open('Untitled.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

modeling_cells = [
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "# 3. Data Preprocessing & Modeling for CareMe Triage Assistant\n",
            "Based on the system objectives for real-time triage recommendation and confidence-aware predictions, we will prepare `df1` by:\n",
            "1. **Selecting Data:** Dropping 'data leakage' columns (events that happen *after* triage like length of stay, discharge disposition, mistriage flags, specific ED diagnosis).\n",
            "2. **Handling Missing Values & Encoding:** Preparing the vitals and chief complaints for the model.\n",
            "3. **Training the Model:** Training the RandomForest to predict the true `KTAS_expert` assigned urgency.\n",
            "4. **Confidence Scoring:** Generating probability vectors alongside predictions."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "from sklearn.impute import SimpleImputer\n",
            "\n",
            "# 1. Define target and drop data leakage columns\n",
            "target = 'KTAS_expert'\n",
            "\n",
            "# Columns that are known AFTER triage is done, or are the target itself\n",
            "leakage_cols = ['Diagnosis in ED', 'Disposition', 'Error_group', 'Length of stay_min', \n",
            "                'KTAS duration_min', 'mistriage', 'KTAS_RN', 'Group', 'Patients number per hour']\n",
            "\n",
            "df_care = df1.drop(columns=[col for col in leakage_cols if col in df1.columns]).copy()\n",
            "\n",
            "# 2. Separate Features (X) and Target (y)\n",
            "# Ensure target has no missing values\n",
            "df_care = df_care.dropna(subset=[target])\n",
            "y = df_care[target].astype(int) # KTAS scores are typically 1, 2, 3, 4, 5\n",
            "X = df_care.drop(columns=[target])\n",
            "\n",
            "# 3. Identify categorical vs numerical columns\n",
            "categorical_cols = X.select_dtypes(include=['object']).columns\n",
            "numerical_cols = X.select_dtypes(exclude=['object']).columns\n",
            "\n",
            "print(\"Features used for real-time prediction:\\n\", list(X.columns))"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# 4. Preprocessing: Impute missing values and encode categorical features\n",
            "from sklearn.compose import ColumnTransformer\n",
            "from sklearn.pipeline import Pipeline\n",
            "from sklearn.preprocessing import OneHotEncoder, StandardScaler\n",
            "\n",
            "# Numerical transformer: fill missing with median and scale\n",
            "numeric_transformer = Pipeline(steps=[\n",
            "    ('imputer', SimpleImputer(strategy='median')),\n",
            "    ('scaler', StandardScaler())\n",
            "])\n",
            "\n",
            "# Categorical transformer: fill missing with mode and one-hot encode\n",
            "categorical_transformer = Pipeline(steps=[\n",
            "    ('imputer', SimpleImputer(strategy='most_frequent')),\n",
            "    ('onehot', OneHotEncoder(handle_unknown='ignore'))\n",
            "])\n",
            "\n",
            "preprocessor = ColumnTransformer(\n",
            "    transformers=[\n",
            "        ('num', numeric_transformer, numerical_cols),\n",
            "        ('cat', categorical_transformer, categorical_cols)\n",
            "    ])\n",
            "\n",
            "X_preprocessed = preprocessor.fit_transform(X)\n",
            "print(\"Shape of processed feature matrix:\", X_preprocessed.shape)"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# 5. Train-Test Split and Handle Imbalanced Classes (SMOTE)\n",
            "X_train, X_test, y_train, y_test = train_split = train_test_split(X_preprocessed, y, test_size=0.2, random_state=42, stratify=y)\n",
            "\n",
            "# Note: We apply SMOTE *only* to training data to prevent data leakage!\n",
            "smote = SMOTE(random_state=42)\n",
            "X_train_resampled, y_train_resampled = smote.fit_resample(X_train, y_train)\n",
            "\n",
            "print(\"Original training target distribution:\\n\", y_train.value_counts())\n",
            "print(\"\\nResampled training target distribution:\\n\", y_train_resampled.value_counts())"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# 6. Train the Model\n",
            "rf_classifier = RandomForestClassifier(n_estimators=200, random_state=42, class_weight='balanced')\n",
            "rf_classifier.fit(X_train_resampled, y_train_resampled)\n",
            "\n",
            "# 7. Generate Predictions & Evaluate\n",
            "y_pred = rf_classifier.predict(X_test)\n",
            "\n",
            "print(\"\\n--- Classification Report ---\")\n",
            "print(classification_report(y_test, y_pred))\n",
            "\n",
            "# Visualizing the Confusion Matrix\n",
            "plt.figure(figsize=(8,6))\n",
            "cm = confusion_matrix(y_test, y_pred)\n",
            "sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', \n",
            "            xticklabels=sorted(y.unique()), yticklabels=sorted(y.unique()))\n",
            "plt.xlabel('Predicted Triage Level')\n",
            "plt.ylabel('Actual Triage Level')\n",
            "plt.title('Confusion Matrix for Triage Predictions')\n",
            "plt.show()"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### Meeting the Objective: Confidence-Aware Predictions\n",
            "The model should not just spit out a recommendation; it needs to output its **confidence score** so doctors and nurses know when to double-check.\n",
            "We use `predict_proba()` to see how strongly the model believes in its top choice."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# 8. Confidence-Aware Test Cases\n",
            "probabilities = rf_classifier.predict_proba(X_test)\n",
            "predictions = rf_classifier.predict(X_test)\n",
            "\n",
            "import numpy as np\n",
            "import pandas as pd\n",
            "\n",
            "# Let's show the first 5 patients in the test set\n",
            "confidence_results = []\n",
            "classes = rf_classifier.classes_\n",
            "\n",
            "for i in range(5):\n",
            "    true_label = y_test.iloc[i]\n",
            "    pred_label = predictions[i]\n",
            "    # Get the confidence percentage for the chosen prediction\n",
            "    confidence = np.max(probabilities[i]) * 100\n",
            "    \n",
            "    # Get second most likely class (for edge cases)\n",
            "    sorted_probs = np.argsort(probabilities[i])[::-1]\n",
            "    second_pred = classes[sorted_probs[1]]\n",
            "    second_conf = probabilities[i][sorted_probs[1]] * 100\n",
            "    \n",
            "    confidence_results.append({\n",
            "        \"True Triage (KTAS)\": true_label,\n",
            "        \"Predicted Triage\": pred_label,\n",
            "        \"Confidence\": f\"{confidence:.1f}%\",\n",
            "        \"Runner-up Prediction\": f\"KTAS {second_pred} ({second_conf:.1f}%)\",\n",
            "        \"Status\": \"✅ Correct\" if true_label == pred_label else \"❌ Incorrect\"\n",
            "    })\n",
            "\n",
            "results_df = pd.DataFrame(confidence_results)\n",
            "display(results_df)\n",
            "\n",
            "print(\"\\nNotice how the model outputs a 'Confidence' percentage. If the confidence is low \\n(e.g., under 60%), the web app can trigger an alert saying: \\n'⚠️ Borderline Case: Please verify vitals and use clinical judgment.'\")"
        ]
    }
]

nb['cells'].extend(modeling_cells)

with open('Untitled.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1)

print("Modeling cells added to notebook.")
