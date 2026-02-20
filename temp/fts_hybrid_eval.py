from rank_bm25 import BM25Okapi
import numpy as np
import pandas as pd

# Assume df_chunks and synthetic_df already exist
# -----------------------------------------------------------------------------
# 1. SETUP BM25 FOR FTS
# -----------------------------------------------------------------------------
print("Setting up BM25 index for Full Text Search evaluation...")
tokenized_corpus = [doc.split(" ") for doc in df_chunks['content'].tolist()]
bm25 = BM25Okapi(tokenized_corpus)

def retrieve_fts(query, df, top_k=5):
    """Retrieve using BM25 Full Text Search"""
    tokenized_query = query.split(" ")
    doc_scores = bm25.get_scores(tokenized_query)
    
    # Get top k indices
    top_k_indices = np.argsort(doc_scores)[::-1][:top_k]
    return df.iloc[top_k_indices]

# -----------------------------------------------------------------------------
# 2. EVALUATE FTS
# -----------------------------------------------------------------------------
if 'synthetic_df' in globals():
    syn_rows_fts = []
    k_values = [1, 3, 5, 10]
    max_k = max(k_values)
    
    print(f"Evaluating FTS retrieval for {len(synthetic_df)} questions...")
    
    for _, row in synthetic_df.iterrows():
        source_id = row["doc_id"]
        question = row["question"]
    
        try:
            retrieved_df = retrieve_fts(question, df_chunks, top_k=max_k)
            retrieved_ids = retrieved_df['chunk_id'].tolist()
        except Exception as e:
            print(f"Error retrieving: {e}")
            continue
    
        for k in k_values:
            ids_at_k = retrieved_ids[:k]
            found = source_id in ids_at_k
            precision = (1.0 if found else 0.0) / k  
            recall = 1.0 if found else 0.0  
    
            syn_rows_fts.append({"metric": "precision", "k": k, "score": precision, "question": question})
            syn_rows_fts.append({"metric": "recall", "k": k, "score": recall, "question": question})
    
    syn_eval_df_fts = pd.DataFrame(syn_rows_fts)
    
    print("\n--- Synthetic Evaluation Results (FTS / BM25) ---\n")
    print(syn_eval_df_fts.groupby(["metric", "k"])["score"].mean().round(4).to_string())
else:
    print("Please generate synthetic_df first!")

# -----------------------------------------------------------------------------
# 3. SETUP HYBRID SEARCH
# -----------------------------------------------------------------------------
# We need the vector model to be available in globals. Assuming 'model' from sentence_transformers
def retrieve_hybrid(query, df, top_k=5, alpha=0.5):
    """
    Retrieve using Hybrid Search (Vector + BM25)
    alpha = 0.0 is pure BM25, alpha = 1.0 is pure Vector
    """
    # Vector Search
    query_embedding = model.encode([query])[0]
    embeddings = np.stack(df['embedding'].values)
    query_norm = query_embedding / np.linalg.norm(query_embedding)
    embeddings_norm = embeddings / np.linalg.norm(embeddings, axis=1)[:, np.newaxis]
    vector_scores = np.dot(embeddings_norm, query_norm)
    
    # Normalize vector scores to 0-1 range
    vector_min, vector_max = vector_scores.min(), vector_scores.max()
    if vector_max > vector_min:
        vector_scores = (vector_scores - vector_min) / (vector_max - vector_min)
    
    # FTS (BM25) Search
    tokenized_query = query.split(" ")
    bm25_scores = bm25.get_scores(tokenized_query)
    
    # Normalize BM25 scores to 0-1 range
    bm25_min, bm25_max = bm25_scores.min(), bm25_scores.max()
    if bm25_max > bm25_min:
        bm25_scores = (bm25_scores - bm25_min) / (bm25_max - bm25_min)
    
    # Combine scores
    hybrid_scores = (alpha * vector_scores) + ((1 - alpha) * bm25_scores)
    
    # Get top k indices
    top_k_indices = np.argsort(hybrid_scores)[::-1][:top_k]
    return df.iloc[top_k_indices]

# -----------------------------------------------------------------------------
# 4. EVALUATE HYBRID
# -----------------------------------------------------------------------------
if 'synthetic_df' in globals() and 'model' in globals():
    syn_rows_hybrid = []
    
    print(f"\nEvaluating Hybrid retrieval for {len(synthetic_df)} questions...")
    
    for _, row in synthetic_df.iterrows():
        source_id = row["doc_id"]
        question = row["question"]
    
        try:
            # We use alpha=0.5 for equal weighting
            retrieved_df = retrieve_hybrid(question, df_chunks, top_k=max_k, alpha=0.5)
            retrieved_ids = retrieved_df['chunk_id'].tolist()
        except Exception as e:
            print(f"Error retrieving: {e}")
            continue
    
        for k in k_values:
            ids_at_k = retrieved_ids[:k]
            found = source_id in ids_at_k
            precision = (1.0 if found else 0.0) / k  
            recall = 1.0 if found else 0.0  
    
            syn_rows_hybrid.append({"metric": "precision", "k": k, "score": precision, "question": question})
            syn_rows_hybrid.append({"metric": "recall", "k": k, "score": recall, "question": question})
    
    syn_eval_df_hybrid = pd.DataFrame(syn_rows_hybrid)
    
    print("\n--- Synthetic Evaluation Results (Hybrid Search alpha=0.5) ---\n")
    print(syn_eval_df_hybrid.groupby(["metric", "k"])["score"].mean().round(4).to_string())
else:
    print("Please ensure synthetic_df and the 'model' variable are defined!")

# -----------------------------------------------------------------------------
# 5. ALL METRICS PLOT
# -----------------------------------------------------------------------------
if all(v in globals() for v in ['syn_eval_df', 'syn_eval_df_fts', 'syn_eval_df_hybrid']):
    import matplotlib.pyplot as plt
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    dfs = {
        'Vector': syn_eval_df,
        'BM25 (FTS)': syn_eval_df_fts,
        'Hybrid': syn_eval_df_hybrid
    }
    
    colors = {'Vector': 'tab:blue', 'BM25 (FTS)': 'tab:green', 'Hybrid': 'tab:purple'}
    
    for name, mdf in dfs.items():
        # Precision
        data_p = mdf[mdf["metric"] == "precision"]
        means_p = data_p.groupby("k")["score"].mean()
        ax1.plot(means_p.index, means_p.values, marker="o", color=colors[name], label=name)
        
        # Recall
        data_r = mdf[mdf["metric"] == "recall"]
        means_r = data_r.groupby("k")["score"].mean()
        ax2.plot(means_r.index, means_r.values, marker="o", color=colors[name], label=name)
        
    ax1.set_xlabel("k")
    ax1.set_ylabel("Precision@k")
    ax1.set_title("Precision Comparison")
    ax1.grid(True)
    ax1.legend()
    ax1.set_ylim(0, 1.05)
    
    ax2.set_xlabel("k")
    ax2.set_ylabel("Recall@k")
    ax2.set_title("Recall Comparison")
    ax2.grid(True)
    ax2.legend()
    ax2.set_ylim(0, 1.05)
    
    plt.tight_layout()
    plt.show()
