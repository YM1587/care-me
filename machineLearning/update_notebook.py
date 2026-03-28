import json

with open('Untitled.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        source = "".join(cell['source'])
        if "df1 = pd.read_csv(" in source and "sep=';'" not in source:
            new_source = source.replace("encoding='latin1',       # bypass UTF-8 issues", "encoding='latin1',\n    sep=';',                 # handle semicolon separated")
            lines = [line + '\n' for line in new_source.split('\n')]
            lines[-1] = lines[-1].rstrip('\n')
            cell['source'] = lines

eda_cell_1 = {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Basic EDA on df1\n",
    "print('-- DF1 Info --')\n",
    "df1.info()\n",
    "\n",
    "print('\\n-- DF1 Missing Values --')\n",
    "print(df1.isnull().sum())\n",
    "\n",
    "print('\\n-- DF1 Summary Stats --')\n",
    "display(df1.describe())"
   ]
}

eda_cell_2 = {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Basic EDA on df2\n",
    "print('-- DF2 Info --')\n",
    "df2.info()\n",
    "\n",
    "print('\\n-- DF2 Missing Values --')\n",
    "print(df2.isnull().sum())\n",
    "\n",
    "print('\\n-- DF2 Summary Stats --')\n",
    "display(df2.describe())"
   ]
}

nb['cells'].extend([eda_cell_1, eda_cell_2])

with open('Untitled.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1)

print("Notebook updated successfully.")
