
import json

notebook_path = '/Users/yeshwanth/Desktop/ai-engineering-fordham/5.you-can-just-build-things.ipynb'

# Code to insert
chunking_code = """def chunk_text(text, chunk_size=1000, overlap=100):
    chunks = []
    if not text:
        return chunks
        
    start = 0
    text_len = len(text)
    
    while start < text_len:
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += (chunk_size - overlap)
        
    return chunks

all_chunks = []

# Iterate over the loaded dataframe
for index, row in df.iterrows():
    filename = row['filename']
    url = row['url']
    content = row['content']
    
    chunks = chunk_text(content)
    
    for chunk in chunks:
        all_chunks.append({
            'filename': filename,
            'url': url,
            'content': chunk
        })

df_chunks = pd.DataFrame(all_chunks)

print(f"Original documents: {len(df)}")
print(f"Total chunks: {len(df_chunks)}")
print(df_chunks.head())
"""

try:
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)

    # Find the cell for "2. Chunk the Documents"
    # It usually follows the markdown cell with that header.
    # We look for the placeholder in a code cell.
    
    target_found = False
    for i, cell in enumerate(nb['cells']):
        if cell['cell_type'] == 'markdown':
            source = "".join(cell['source'])
            if "# 2. Chunk the Documents" in source:
                # The next cell *should* be the code cell
                if i + 1 < len(nb['cells']) and nb['cells'][i+1]['cell_type'] == 'code':
                    nb['cells'][i+1]['source'] = chunking_code.splitlines(keepends=True)
                    target_found = True
                    print("Updated chunking cell.")
                    break
    
    if not target_found:
        print("Could not find the chunking cell to update.")
    else:
        with open(notebook_path, 'w', encoding='utf-8') as f:
            json.dump(nb, f, indent=1)
        print("Notebook saved.")

except Exception as e:
    print(f"Error: {e}")
