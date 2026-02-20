import json

with open('/Users/yeshwanth/Desktop/ai-engineering-fordham/5.you-can-just-build-things.ipynb', 'r') as f:
    nb = json.load(f)

for cell in nb['cells']:
    if 'source' in cell:
        for i, line in enumerate(cell['source']):
            cell['source'][i] = line.replace('data/fordham-website', 'fordham_chatbot/data/fordham-website')

with open('/Users/yeshwanth/Desktop/ai-engineering-fordham/5.you-can-just-build-things.ipynb', 'w') as f:
    json.dump(nb, f, indent=1)
