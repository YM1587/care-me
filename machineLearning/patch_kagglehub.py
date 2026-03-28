import json

with open('Untitled.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        source = "".join(cell['source'])
        if 'kagglehub.dataset_download' in source:
            cell['source'] = [
                "path1 = '.'\n",
                "path2 = '.'\n",
                "print('Using local paths for data.')"
            ]
        elif 'print(os.listdir(path1))' in source:
            pass # leave it, os.listdir('.') is fine

with open('Untitled.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1)

print("Notebook paths patched.")
