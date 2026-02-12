
import json

notebook_path = '/Users/yeshwanth/Desktop/ai-engineering-fordham/5.you-can-just-build-things.ipynb'

# Improved loading code that handles directory fallback
new_loading_code = """import zipfile
import pandas as pd
import os
import pathlib

def load_fordham_data(source_path):
    data = []
    
    # Check if it's a zip file
    if source_path.endswith('.zip') and os.path.exists(source_path):
        print(f"Loading from zip: {source_path}")
        with zipfile.ZipFile(source_path, 'r') as z:
            file_list = [f for f in z.namelist() if f.endswith('.md')]
            for file_name in file_list:
                with z.open(file_name) as f:
                    try:
                        content = f.read().decode('utf-8')
                    except UnicodeDecodeError:
                        continue
                    
                    lines = content.split('\\n', 1)
                    url = lines[0].strip() if lines else ""
                    body = lines[1].strip() if len(lines) > 1 else ""
                    
                    data.append({
                        "filename": file_name,
                        "url": url,
                        "content": body
                    })
                    
    # Check if it's a directory
    elif os.path.exists(source_path) and os.path.isdir(source_path):
        print(f"Loading from directory: {source_path}")
        path = pathlib.Path(source_path)
        files = list(path.glob('*.md'))
        
        for file_path in files:
             try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    if not lines: continue
                    
                    url = lines[0].strip()
                    content = "".join(lines[1:]).strip()
                    
                    data.append({
                        "filename": file_path.name,
                        "url": url,
                        "content": content
                    })
             except Exception as e:
                print(f"Error reading {file_path}: {e}")
                
    else:
        print(f"Source not found or invalid: {source_path}")
        # Try default locations if provided path fails?
        # Let's inspect data/fordham-website just in case user passed zip but has dir
        fallback_dir = 'data/fordham-website'
        if source_path != fallback_dir and os.path.exists(fallback_dir) and os.path.isdir(fallback_dir):
             print(f"Fallback: Loading from {fallback_dir}")
             return load_fordham_data(fallback_dir) # Recursive call to load from dir
             
        return pd.DataFrame()

    return pd.DataFrame(data)

# Usage
# Try zip first, but function handles fallback if zip is missing but dir exists
source_path = 'data/fordham-website.zip' 
if not os.path.exists(source_path):
    # If zip is missing, point to the directory we know likely exists
    source_path = 'data/fordham-website'

df = load_fordham_data(source_path)

if len(df) == 0:
    print("WARNING: No data loaded! Check your data directory.")
else:
    print(f"Loaded {len(df)} documents.")
    print(df.head())
"""

try:
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)

    # Update the loading cell (implementation of Task 1)
    target_found = False
    for i, cell in enumerate(nb['cells']):
        if cell['cell_type'] == 'markdown':
            source = "".join(cell['source'])
            if "# 1. Look at your data" in source: # Task 1 header
                 # Look for code cell
                 if i + 1 < len(nb['cells']) and nb['cells'][i+1]['cell_type'] == 'code':
                     nb['cells'][i+1]['source'] = new_loading_code.splitlines(keepends=True)
                     target_found = True
                     print("Updated data loading cell with robust fallback.")
                     break
                     
    if not target_found:
        print("Could not find the data loading cell.")
    else:
        with open(notebook_path, 'w', encoding='utf-8') as f:
             json.dump(nb, f, indent=1)
        print("Notebook saved.")

except Exception as e:
    print(f"Error: {e}")
