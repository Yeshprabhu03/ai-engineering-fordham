import json

path = '/Users/yeshwanth/Desktop/ai-engineering-fordham/5.you-can-just-build-things.ipynb'
with open(path, 'r') as f:
    nb = json.load(f)

for cell in nb.get('cells', []):
    if cell.get('cell_type') == 'code':
        new_source = []
        for line in cell.get('source', []):
            # Fix lines that incorrectly have a literal \n (backslash + n) at the end 
            if line.endswith('\\n\n'):
                line = line[:-3] + '\n'
            elif line.endswith('\\n'):
                line = line[:-2]
            new_source.append(line)
        cell['source'] = new_source

with open(path, 'w') as f:
    json.dump(nb, f, indent=1)
