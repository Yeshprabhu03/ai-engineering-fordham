
import json

notebook_path = '/Users/yeshwanth/Desktop/ai-engineering-fordham/5.you-can-just-build-things.ipynb'

# Code to insert
embedding_code = """from sentence_transformers import SentenceTransformer
import numpy as np

# 1. Initialize the model
# 'all-MiniLM-L6-v2' is a small, fast model great for local use
model = SentenceTransformer('all-MiniLM-L6-v2')

# 2. Sample 10% of the data to speed up processing
print(f"Original dataframe size: {len(df_chunks)}")
# Use a fixed random state for reproducibility
df_chunks = df_chunks.sample(frac=0.1, random_state=42).reset_index(drop=True)
print(f"Sampled dataframe size: {len(df_chunks)}")

# 3. Get the list of texts to embed
# We use the 'content' column of our chunks dataframe
chunk_texts = df_chunks['content'].tolist()

print(f"Embedding {len(chunk_texts)} chunks...")

# 4. Embed the chunks
# The model handles batching automatically
embeddings = model.encode(chunk_texts, show_progress_bar=True)

# 5. Add embeddings to the dataframe 
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
