
import json

notebook_path = '/Users/yeshwanth/Desktop/ai-engineering-fordham/5.you-can-just-build-things.ipynb'

# Code to insert
embedding_code = """from sentence_transformers import SentenceTransformer
import numpy as np

# Initialize the model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Get the list of texts to embed
chunk_texts = df_chunks['content'].tolist()

print(f"Embedding {len(chunk_texts)} chunks...")

# Embed the chunks
# show_progress_bar=True is nice but might not show up well in non-interactive run, but good for notebook
embeddings = model.encode(chunk_texts, show_progress_bar=True)

# Add embeddings to the dataframe 
# We can store them as a list/array in a new column
df_chunks['embedding'] = list(embeddings)

print("Embedding complete.")
print(df_chunks.head())
"""

try:
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)

    # Find the cell for "3. Embed the Chunks"
    target_found = False
    for i, cell in enumerate(nb['cells']):
        if cell['cell_type'] == 'markdown':
            source = "".join(cell['source'])
            if "# 3. Embed the Chunks" in source:
                # The next cell *should* be the code cell
                if i + 1 < len(nb['cells']) and nb['cells'][i+1]['cell_type'] == 'code':
                    nb['cells'][i+1]['source'] = embedding_code.splitlines(keepends=True)
                    target_found = True
                    print("Updated embedding cell.")
                    break
    
    if not target_found:
        print("Could not find the embedding cell to update.")
    else:
        with open(notebook_path, 'w', encoding='utf-8') as f:
            json.dump(nb, f, indent=1)
        print("Notebook saved.")

except Exception as e:
    print(f"Error: {e}")
