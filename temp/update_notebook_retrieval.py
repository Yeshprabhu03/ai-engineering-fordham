
import json

notebook_path = '/Users/yeshwanth/Desktop/ai-engineering-fordham/5.you-can-just-build-things.ipynb'

# Code to insert
retrieval_code = """import numpy as np

def retrieve(query, df, top_k=5):
    # Embed the query
    query_embedding = model.encode([query])[0]
    
    # Calculate cosine similarity
    # Stack the embeddings from the dataframe
    embeddings = np.stack(df['embedding'].values)
    
    # Normalize query and embeddings for cosine similarity
    # (SentenceTransformer embeddings are usually normalized, but good practice)
    query_norm = query_embedding / np.linalg.norm(query_embedding)
    embeddings_norm = embeddings / np.linalg.norm(embeddings, axis=1)[:, np.newaxis]
    
    # Dot product
    scores = np.dot(embeddings_norm, query_norm)
    
    # valid_indices = np.argsort(scores)[::-1][:top_k] # This is slow for large arrays but fine here
    
    # Get top k indices
    # We can use argpartition for faster top-k
    top_k_indices = np.argpartition(scores, -top_k)[-top_k:]
    top_k_indices = top_k_indices[np.argsort(scores[top_k_indices])][::-1]
    
    # Return the top k rows
    return df.iloc[top_k_indices]

# Test it
results = retrieve("financial aid", df_chunks)
for i, row in results.iterrows():
    print(f"URL: {row['url']}")
    print(f"Content: {row['content'][:150]}...")
    print("-" * 20)
"""

try:
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)

    # Find the cell for "4. Retrieve"
    target_found = False
    for i, cell in enumerate(nb['cells']):
        if cell['cell_type'] == 'markdown':
            source = "".join(cell['source'])
            if "# 4. Retrieve" in source:
                # The next cell *should* be the code cell
                if i + 1 < len(nb['cells']) and nb['cells'][i+1]['cell_type'] == 'code':
                    nb['cells'][i+1]['source'] = retrieval_code.splitlines(keepends=True)
                    target_found = True
                    print("Updated retrieval cell.")
                    break
    
    if not target_found:
        print("Could not find the retrieval cell to update.")
    else:
        with open(notebook_path, 'w', encoding='utf-8') as f:
            json.dump(nb, f, indent=1)
        print("Notebook saved.")

except Exception as e:
    print(f"Error: {e}")
