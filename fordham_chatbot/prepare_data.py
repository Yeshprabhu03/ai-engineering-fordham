import pandas as pd
import os
import zipfile
import pathlib
import numpy as np
import openai
from dotenv import load_dotenv
import argparse
import time

load_dotenv()

# Configuration
DATA_PATH = 'data/fordham-website'
OUTPUT_PATH = 'data/processed_fordham.pkl'
MODEL_NAME = 'text-embedding-3-small'

def load_and_chunk_data(source_path):
    print(f"Loading data from {source_path}...")
    data = []
    
    # Check zip
    if source_path.endswith('.zip') and os.path.exists(source_path):
        with zipfile.ZipFile(source_path, 'r') as z:
            file_list = [f for f in z.namelist() if f.endswith('.md')]
            for file_name in file_list:
                with z.open(file_name) as f:
                    try:
                        content = f.read().decode('utf-8')
                        lines = content.split('\n', 1)
                        url = lines[0].strip() if lines else ""
                        body = lines[1].strip() if len(lines) > 1 else ""
                        data.append({"filename": file_name, "url": url, "content": body})
                    except: continue

    # Check directory
    elif os.path.exists(source_path) and os.path.isdir(source_path):
        path = pathlib.Path(source_path)
        files = list(path.glob('*.md'))
        for file_path in files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    if not lines: continue
                    url = lines[0].strip()
                    content = "".join(lines[1:]).strip()
                    data.append({"filename": file_path.name, "url": url, "content": content})
            except: continue
            
    df = pd.DataFrame(data)
    if df.empty: 
        print("No data found.")
        return pd.DataFrame()
        
    print(f"Found {len(df)} documents.")
    # Removing sampling to process full dataset
    # df = df.sample(frac=0.01, random_state=42) 
    
    # Chunking Logic (Same as before)
    print("Chunking data...")
    all_chunks = []
    chunk_size = 1000
    overlap = 100
    
    for index, row in df.iterrows():
        content = row.get('content', '')
        if not isinstance(content, str): continue
        
        start = 0
        text_len = len(content)
        
        while start < text_len:
            end = start + chunk_size
            chunk = content[start:end]
            if chunk.strip():
                all_chunks.append({
                    'filename': row['filename'],
                    'url': row['url'],
                    'content': chunk
                })
            start += (chunk_size - overlap)
            
    return pd.DataFrame(all_chunks)

def generate_embeddings(df_chunks):
    print(f"Generating embeddings using OpenAI ({MODEL_NAME})...")
    client = openai.OpenAI()
    
    texts = df_chunks['content'].tolist()
    embeddings = []
    
    batch_size = 50
    total_batches = (len(texts) + batch_size - 1) // batch_size
    
    print(f"Processing {len(texts)} chunks in {total_batches} batches...")
    
    for i in range(0, len(texts), batch_size):
        # Retry logic
        max_retries = 5
        for attempt in range(max_retries):
            try:
                time.sleep(0.2) # Base rate limit safety
                batch = texts[i:i + batch_size]
                response = client.embeddings.create(input=batch, model=MODEL_NAME)
                batch_embeddings = [item.embedding for item in response.data]
                embeddings.extend(batch_embeddings)
                print(f"Batch {i//batch_size + 1}/{total_batches} done.")
                break # Success
            except Exception as e:
                err_str = str(e).lower()
                if "rate_limit" in err_str or "429" in err_str:
                     if attempt < max_retries - 1:
                        wait = 2 ** attempt * 5
                        print(f"Rate limit hit. Retrying in {wait}s...")
                        time.sleep(wait)
                        continue
                print(f"Error in batch {i}: {e}")
                raise e
                
    return embeddings

def main():
    parser = argparse.ArgumentParser(description="Process Fordham data for RAG.")
    parser.add_argument("--limit", type=int, help="Limit the number of chunks to process (for testing).")
    args = parser.parse_args()

    # Load Data
    data_path = DATA_PATH
    # Check if directory exists, else check zip
    if not os.path.exists(data_path) and os.path.exists(data_path + '.zip'):
        data_path = data_path + '.zip'
    
    if not os.path.exists(data_path):
        print(f"Error: Data not found at {DATA_PATH} or {data_path}")
        return

    df = load_and_chunk_data(data_path)
    
    if df.empty:
        print("No chunks created.")
        return
    
    if args.limit:
        print(f"Limiting to {args.limit} chunks (from {len(df)} total)...")
        df = df.head(args.limit)

    print(f"Generated {len(df)} chunks.")
    
    embeddings = generate_embeddings(df)
    print(f"Converting embeddings to numpy array (float32)...")
    embeddings_array = np.array(embeddings, dtype=np.float32)
    
    # Save Embeddings separately
    np.save('data/embeddings.npy', embeddings_array)
    print(f"Saved embeddings to data/embeddings.npy")
    
    # Save DataFrame without embeddings (lightweight)
    df_corpus = df.drop(columns=['embedding'], errors='ignore')
    df_corpus.to_pickle('data/corpus.pkl')
    print(f"Saved {len(df_corpus)} text records to data/corpus.pkl")
    
    print("Done!")

if __name__ == "__main__":
    main()
