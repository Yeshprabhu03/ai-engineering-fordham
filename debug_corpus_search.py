import pandas as pd
import os

# Set up paths
base_dir = "fordham_chatbot"
corpus_path = os.path.join(base_dir, "data", "corpus.pkl")

# Load existing corpus
print(f"Loading corpus from {corpus_path}...")
df = pd.read_pickle(corpus_path)
print(f"Loaded {len(df)} chunks.")

# Search for relevant terms
search_terms = ["tuition", "fee", "cost", "price", "financial aid", "MBA"]
hits = []

for idx, row in df.iterrows():
    content = row['content'].lower()
    # Check if ANY term is in content
    matches = [term for term in search_terms if term in content]
    if matches:
        score = len(matches) # Simple relevance proxy
        hits.append({
            "filename": row['filename'],
            "content": row['content'][:300], # Preview
            "matches": matches,
            "match_count": score
        })

# Sort by relevance 
hits.sort(key=lambda x: x['match_count'], reverse=True)

print(f"\nFound {len(hits)} possibly relevant chunks.\n")
for i, hit in enumerate(hits[:10]):
    print(f"Rank {i+1} ({hit['match_count']} matches): {hit['filename']}")
    print(f"Content: {hit['content']}...\n")
