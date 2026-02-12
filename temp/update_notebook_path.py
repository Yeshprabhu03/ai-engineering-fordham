
import json

notebook_path = '/Users/yeshwanth/Desktop/ai-engineering-fordham/5.you-can-just-build-things.ipynb'

# Update the usage code to point to the directory
new_usage_code = """# Usage
source_path = 'data/fordham-website' # Pointing directly to the directory as confirmed
if not os.path.exists(source_path):
    print(f"Warning: Path {source_path} does not exist relative to notebook.")

df = load_fordham_data(source_path)
print(f"Loaded {len(df)} documents.")
print(df.head())
"""

try:
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)

    # Find the data loading cell
    # My previous update put the function AND usage in the same cell.
    # I need to be careful not to overwrite the function definition.
    # The previous cell content ended with:
    # # Usage
    # zip_path = 'data/fordham-website.zip'
    # df = load_fordham_data(zip_path)
    # ...
    
    # I will look for the cell containing "def load_fordham_data" and update the usage part.
    
    updated = False
    for cell in nb['cells']:
        if cell['cell_type'] == 'code':
            source = "".join(cell['source'])
            if "def load_fordham_data" in source:
                # Split source to keep the function definition but replace the usage part
                if "# Usage" in source:
                    parts = source.split("# Usage")
                    new_source = parts[0] + new_usage_code
                    cell['source'] = new_source.splitlines(keepends=True)
                    updated = True
                    print("Updated usage code in data loading cell.")
                    break
    
    if not updated:
        print("Could not find the function definition or '# Usage' marker.")

    if updated:
        with open(notebook_path, 'w', encoding='utf-8') as f:
            json.dump(nb, f, indent=1)
        print("Notebook saved.")

except Exception as e:
    print(f"Error: {e}")
