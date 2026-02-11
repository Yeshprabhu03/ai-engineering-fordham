
import json
import os

notebook_path = '/Users/yeshwanth/Desktop/ai-engineering-fordham/5.you-can-just-build-things.ipynb'
target_string = "# Placeholder for your implementation"

user_code = """import zipfile
import pandas as pd
import os

def load_fordham_data(zip_path):
    data = []
    
    if not os.path.exists(zip_path):
        print(f"Zip file not found: {zip_path}")
        # Fallback to directory if zip is missing but directory exists?
        # For now, just return empty or error
        return pd.DataFrame()

    with zipfile.ZipFile(zip_path, 'r') as z:
        # Get list of all files in the zip
        file_list = [f for f in z.namelist() if f.endswith('.md')]
        
        for file_name in file_list:
            with z.open(file_name) as f:
                # Read content and decode to string
                try:
                    content = f.read().decode('utf-8')
                except UnicodeDecodeError:
                    continue
                
                # Split the first line (URL) from the rest of the text
                lines = content.split('\\n', 1)
                url = lines[0].strip() if lines else ""
                body = lines[1].strip() if len(lines) > 1 else ""
                
                data.append({
                    "filename": file_name,
                    "url": url,
                    "content": body
                })
                
    return pd.DataFrame(data)

# Usage
zip_path = 'data/fordham-website.zip'
df = load_fordham_data(zip_path)
print(f"Loaded {len(df)} documents.")
print(df.head())
"""

try:
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)

    updated = False
    for cell in nb['cells']:
        if cell['cell_type'] == 'code':
            source = "".join(cell['source'])
            if target_string in source or "def load_data(data_dir):" in source:
                cell['source'] = user_code.splitlines(keepends=True)
                updated = True
                print("Updated cell with user code.")
                break
    
    if not updated:
        # If we didn't find the placeholder (maybe previous edit sort of worked?), try the second code cell
        # The prompt says "Implement the cell following '1. Look at your data'" which is likely the first code cell index 2 (0-indexed) or around there.
        # Let's try to be smart or just report failure.
        print("Could not find placeholder to update.")
    else:
        with open(notebook_path, 'w', encoding='utf-8') as f:
            json.dump(nb, f, indent=1)
        print("Notebook saved.")

except Exception as e:
    print(f"Error: {e}")
