import json

with open('Untitled.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

metrics_cells = [
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### Dedicated Evaluation Metrics\n",
            "Let's explicitly calculate and visualize the core performance metrics (Accuracy, Precision, Recall, F1-Score) to see exactly how the model performs overall, especially important for clinical applications where we need high precision."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score\n",
            "import pandas as pd\n",
            "import matplotlib.pyplot as plt\n",
            "import seaborn as sns\n",
            "\n",
            "# Calculate metrics (using weighted average due to multi-class imbalance)\n",
            "acc = accuracy_score(y_test, y_pred)\n",
            "prec = precision_score(y_test, y_pred, average='weighted')\n",
            "rec = recall_score(y_test, y_pred, average='weighted')\n",
            "f1 = f1_score(y_test, y_pred, average='weighted')\n",
            "\n",
            "# Format into a DataFrame for a clean table view\n",
            "metrics_df = pd.DataFrame({\n",
            "    \"Metric\": [\"Accuracy\", \"Precision (Weighted)\", \"Recall (Weighted)\", \"F1-Score (Weighted)\"],\n",
            "    \"Score\": [f\"{acc:.4f}\", f\"{prec:.4f}\", f\"{rec:.4f}\", f\"{f1:.4f}\"]\n",
            "})\n",
            "\n",
            "display(metrics_df)\n",
            "\n",
            "# Visualizing the metrics\n",
            "plt.figure(figsize=(8, 5))\n",
            "metrics_values = [acc, prec, rec, f1]\n",
            "metrics_names = [\"Accuracy\", \"Precision\", \"Recall\", \"F1-Score\"]\n",
            "\n",
            "sns.barplot(x=metrics_names, y=metrics_values, palette=\"viridis\")\n",
            "for i, v in enumerate(metrics_values):\n",
            "    plt.text(i, v + 0.01, f\"{v:.2f}\", ha='center', fontsize=12)\n",
            "\n",
            "plt.ylim(0, 1.1)\n",
            "plt.title(\"Overall Model Evaluation Metrics\")\n",
            "plt.ylabel(\"Score\")\n",
            "plt.show()"
        ]
    }
]

nb['cells'].extend(metrics_cells)

with open('Untitled.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1)

print("Metrics cells added to notebook.")
