import json

with open('Untitled.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Optional: filter out the old basic EDA cells if they are exactly what we added before.
# We'll just replace the last two basic EDA cells or just append. 
# actually, better to just append deep EDA cells.

deep_eda_cells = [
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "# Deep Exploratory Data Analysis (EDA)\n",
            "This section provides deeper insights into both datasets to help you decide which one best suits the \"CareMe\" idea (Emergency Triage vs. ICU Patient Monitoring)."
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 1. Deep EDA on DF1 (Emergency Triage)\n",
            "Let's look at the distribution of some crucial features, such as `Disposition` (whether a patient is admitted or discharged) and `mistriage` (was the initial assessment correct?)."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "import matplotlib.pyplot as plt\n",
            "import seaborn as sns\n",
            "\n",
            "sns.set_theme(style=\"whitegrid\")\n",
            "\n",
            "# 1. Plotting the target variables for Triage: Disposition and Mistriage\n",
            "fig, axes = plt.subplots(1, 2, figsize=(14, 5))\n",
            "\n",
            "if 'Disposition' in df1.columns:\n",
            "    sns.countplot(data=df1, x='Disposition', ax=axes[0], palette='viridis')\n",
            "    axes[0].set_title('Distribution of Disposition (DF1)')\n",
            "\n",
            "if 'mistriage' in df1.columns:\n",
            "    sns.countplot(data=df1, x='mistriage', ax=axes[1], palette='magma')\n",
            "    axes[1].set_title('Distribution of Mistriage (DF1)')\n",
            "\n",
            "plt.tight_layout()\n",
            "plt.show()"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# 2. Correlation heatmap for DF1 (Numeric columns only)\n",
            "plt.figure(figsize=(10, 8))\n",
            "numeric_df1 = df1.select_dtypes(include=['float64', 'int64'])\n",
            "if not numeric_df1.empty:\n",
            "    corr1 = numeric_df1.corr()\n",
            "    sns.heatmap(corr1, cmap='coolwarm', annot=False, fmt=\".2f\")\n",
            "    plt.title('Correlation Heatmap for Triage Data (DF1)')\n",
            "    plt.show()"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 2. Deep EDA on DF2 (ICU Mortality Prediction)\n",
            "Now let's analyze the ICU patient dataset. Important target labels here are `mortality_label` and `sepsis_flag`."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# 1. Plotting target variables for ICU Data\n",
            "fig, axes = plt.subplots(1, 2, figsize=(14, 5))\n",
            "\n",
            "if 'mortality_label' in df2.columns:\n",
            "    sns.countplot(data=df2, x='mortality_label', ax=axes[0], palette='Blues_r')\n",
            "    axes[0].set_title('Distribution of Mortality Label (DF2)')\n",
            "\n",
            "if 'sepsis_flag' in df2.columns:\n",
            "    sns.countplot(data=df2, x='sepsis_flag', ax=axes[1], palette='Reds_r')\n",
            "    axes[1].set_title('Distribution of Sepsis Flag (DF2)')\n",
            "\n",
            "plt.tight_layout()\n",
            "plt.show()"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# 2. Distribution of some vital signs\n",
            "fig, axes = plt.subplots(1, 4, figsize=(20, 5))\n",
            "cols_to_plot = ['heart_rate_mean', 'systolic_bp_mean', 'glucose_mean', 'lactate_mean']\n",
            "\n",
            "for i, col in enumerate(cols_to_plot):\n",
            "    if col in df2.columns:\n",
            "        sns.histplot(df2[col].dropna(), bins=30, kde=True, ax=axes[i], color='teal')\n",
            "        axes[i].set_title(f'Distribution of {col}')\n",
            "        \n",
            "plt.tight_layout()\n",
            "plt.show()"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# 3. Correlation heatmap for DF2 (Numeric columns only)\n",
            "plt.figure(figsize=(12, 10))\n",
            "numeric_df2 = df2.select_dtypes(include=['float64', 'int64'])\n",
            "if not numeric_df2.empty:\n",
            "    corr2 = numeric_df2.corr()\n",
            "    sns.heatmap(corr2, cmap='YlGnBu', annot=False)\n",
            "    plt.title('Correlation Heatmap for ICU Data (DF2)')\n",
            "    plt.show()"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### Summary & Decision Framework\n",
            "- **Option 1: Triage Application (`df1`):** Predicts patient disposition and avoids mistriage in Emergency Services. Great for applications aiming to streamline ER patient intake.\n",
            "- **Option 2: ICU Patient Monitoring (`df2`):** Predicts patient mortality and sepsis based on vital signs in an ICU context. More focused on critical care outcomes.\n",
            "\n",
            "Depending on whether your \"CareMe\" app is focusing on **patient intake (ER)** or **critical condition monitoring (ICU)**, you can select the most appropriate dataset."
        ]
    }
]

nb['cells'].extend(deep_eda_cells)

with open('Untitled.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1)

print("Deep EDA cells added to notebook.")
