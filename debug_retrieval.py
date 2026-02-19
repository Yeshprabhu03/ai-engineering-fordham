import pandas as pd
import numpy as np
import openai
import os
import pickle
from rank_bm25 import BM25Okapi
from dotenv import load_dotenv

load_dotenv(dotenv_path='fordham_chatbot/.env')

# Load Data
base_dir = 'fordham_chatbot'
corpus_path = os.path.join(base_dir, 'data', 'corpus.pkl')
embeddings_path = os.path.join(base_dir, 'data', 'embeddings.npy')
bm25_path = os.path.join(base_dir, 'data', 'bm25_index.pkl')

print("Loading data...")
df = pd.read_pickle(corpus_path)
embeddings = np.load(embeddings_path)
with open(bm25_path, 'rb') as f:
    bm25 = pickle.load(f)

# Query
query = "What was the tuition rate per credit for students who entered prior to Fall 2017?"
print(f"\nQuery: {query}")

# Vector Search
client = openai.OpenAI()
resp = client.embeddings.create(input=query, model="text-embedding-3-small")
q_embed = resp.data[0].embedding
q_norm = q_embed / np.linalg.norm(q_embed)
e_norm = embeddings / np.linalg.norm(embeddings, axis=1)[:, np.newaxis]
vec_scores = np.dot(e_norm, q_norm)

# BM25 Search
tokenized_query = query.lower().split()
bm25_scores = bm25.get_scores(tokenized_query)
if bm25_scores.max() > 0:
    bm25_scores = bm25_scores / bm25_scores.max()

# Hybrid
alpha = 0.3
final_scores = (vec_scores * (1 - alpha)) + (bm25_scores * alpha)

# Top 10
top_k = 10
top_indices = np.argsort(final_scores)[::-1][:top_k]
results = df.iloc[top_indices]

print(f"\nTop 5 Results:")
for i, row in results.iterrows():
    print(f"--- Score: {final_scores[i]:.4f} (Vec: {vec_scores[i]:.4f}, BM25: {bm25_scores[i]:.4f}) ---")
    print(f"File: {row['filename']}")
    print(f"Content: {row['content'][:200]}...\n")
