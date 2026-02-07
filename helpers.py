"""
Helpers module for AI Engineering: data loading, BM25, evaluation, embeddings.
Used by 4.embeddings-semantic-search.ipynb and related notebooks.
"""

from pathlib import Path
from collections import Counter
import string

import pandas as pd
import numpy as np

# ---------------------------------------------------------------------------
# Data loading (WANDS dataset)
# ---------------------------------------------------------------------------

def load_wands_products(data_dir: str = "data") -> pd.DataFrame:
    """Load WANDS products from local file."""
    filepath = Path(data_dir) / "wayfair-products.csv"
    products = pd.read_csv(filepath, sep='\t')
    products = products.rename(columns={'category hierarchy': 'category_hierarchy'})
    return products


def load_wands_queries(data_dir: str = "data") -> pd.DataFrame:
    """Load WANDS queries from local file."""
    filepath = Path(data_dir) / "wayfair-queries.csv"
    return pd.read_csv(filepath, sep='\t')


def load_wands_labels(data_dir: str = "data") -> pd.DataFrame:
    """Load WANDS relevance labels from local file."""
    filepath = Path(data_dir) / "wayfair-labels.csv"
    labels = pd.read_csv(filepath, sep='\t')
    grade_map = {'Exact': 2, 'Partial': 1, 'Irrelevant': 0}
    labels['grade'] = labels['label'].map(grade_map)
    return labels


# ---------------------------------------------------------------------------
# Default tokenizer (Snowball) and BM25
# ---------------------------------------------------------------------------

def _default_tokenizer():
    """Lazy-init default Snowball tokenizer."""
    import Stemmer
    _stemmer = Stemmer.Stemmer('english')
    _punct_trans = str.maketrans({key: ' ' for key in string.punctuation})

    def tokenize(text):
        if pd.isna(text) or text is None:
            return []
        text = str(text).translate(_punct_trans)
        tokens = text.lower().split()
        return [_stemmer.stemWord(t) for t in tokens]
    return tokenize


_tokenizer = None

def snowball_tokenize(text: str) -> list:
    """Tokenize text with Snowball stemming."""
    global _tokenizer
    if _tokenizer is None:
        _tokenizer = _default_tokenizer()
    return _tokenizer(text)


def build_index(docs: list, tokenizer=None):
    """
    Build an inverted index from a list of documents.
    If tokenizer is None, uses snowball_tokenize.
    Returns (index, doc_lengths).
    """
    if tokenizer is None:
        tokenizer = snowball_tokenize
    index = {}
    doc_lengths = []
    for doc_id, doc in enumerate(docs):
        tokens = tokenizer(doc)
        doc_lengths.append(len(tokens))
        term_counts = Counter(tokens)
        for term, count in term_counts.items():
            if term not in index:
                index[term] = {}
            index[term][doc_id] = count
    return index, doc_lengths


def _get_df(term: str, index: dict) -> int:
    if term in index:
        return len(index[term])
    return 0


def _bm25_idf(df: int, num_docs: int) -> float:
    return np.log((num_docs - df + 0.5) / (df + 0.5) + 1)


def _bm25_tf(tf: int, doc_len: int, avg_doc_len: float, k1: float = 1.2, b: float = 0.75) -> float:
    return (tf * (k1 + 1)) / (tf + k1 * (1 - b + b * doc_len / avg_doc_len))


def score_bm25(query: str, index: dict, num_docs: int, doc_lengths: list, tokenizer=None,
               k1: float = 1.2, b: float = 0.75) -> np.ndarray:
    """Score all documents using BM25. Uses snowball_tokenize if tokenizer is None."""
    if tokenizer is None:
        tokenizer = snowball_tokenize
    query_tokens = tokenizer(query)
    scores = np.zeros(num_docs)
    avg_doc_len = np.mean(doc_lengths) if doc_lengths else 1.0
    for token in query_tokens:
        df = _get_df(token, index)
        if df == 0:
            continue
        idf = _bm25_idf(df, num_docs)
        if token in index:
            for doc_id, tf in index[token].items():
                tf_norm = _bm25_tf(tf, doc_lengths[doc_id], avg_doc_len, k1, b)
                scores[doc_id] += idf * tf_norm
    return scores


def search_bm25(query: str, index: dict, products_df: pd.DataFrame, doc_lengths: list,
                k: int = 10, tokenizer=None) -> pd.DataFrame:
    """Search products with BM25 and return top-k results with bm25_score column."""
    num_docs = len(products_df)
    scores = score_bm25(query, index, num_docs, doc_lengths, tokenizer=tokenizer)
    top_k_idx = np.argsort(-scores)[:k]
    results = products_df.iloc[top_k_idx].copy()
    results['bm25_score'] = scores[top_k_idx]
    results['rank'] = range(1, k + 1)
    return results


# ---------------------------------------------------------------------------
# Evaluation (NDCG)
# ---------------------------------------------------------------------------

def _get_relevance_grades(product_ids: list, query_id: int, labels_df: pd.DataFrame) -> list:
    query_labels = labels_df[labels_df['query_id'] == query_id]
    label_dict = dict(zip(query_labels['product_id'], query_labels['grade']))
    return [label_dict.get(pid, 0) for pid in product_ids]


def _calculate_dcg(relevances: list, k: int) -> float:
    relevances = np.array(relevances[:k])
    gains = 2 ** relevances - 1
    discounts = np.log2(np.arange(2, k + 2))
    return float(np.sum(gains / discounts))


def _calculate_ndcg(relevances: list, k: int) -> float:
    dcg = _calculate_dcg(relevances, k)
    ideal = sorted(relevances, reverse=True)
    idcg = _calculate_dcg(ideal, k)
    return dcg / idcg if idcg > 0 else 0.0


def _evaluate_single_query(query_text: str, query_id: int, products_df: pd.DataFrame,
                          labels_df: pd.DataFrame, search_func, k: int = 10) -> float:
    results = search_func(query_text)
    product_ids = results['product_id'].tolist()[:k]
    relevances = _get_relevance_grades(product_ids, query_id, labels_df)
    return _calculate_ndcg(relevances, k)


def evaluate_search(search_func, products_df: pd.DataFrame, queries_df: pd.DataFrame,
                    labels_df: pd.DataFrame, k: int = 10, verbose: bool = True) -> pd.DataFrame:
    """Evaluate search across all queries. search_func takes query string, returns DataFrame with product_id."""
    results = []
    for _, row in queries_df.iterrows():
        query_id = row['query_id']
        query_text = row['query']
        ndcg = _evaluate_single_query(query_text, query_id, products_df, labels_df, search_func, k)
        results.append({'query_id': query_id, 'query': query_text, 'ndcg': ndcg})
    results_df = pd.DataFrame(results)
    if verbose:
        print(f"Evaluated {len(results_df)} queries")
        print(f"Mean NDCG@{k}: {results_df['ndcg'].mean():.4f}")
    return results_df


# ---------------------------------------------------------------------------
# Embeddings (local model) and similarity
# ---------------------------------------------------------------------------

_model_cache = {}

def get_local_model(model_name: str = "all-MiniLM-L6-v2"):
    """Load a sentence-transformers model (cached)."""
    if model_name not in _model_cache:
        from sentence_transformers import SentenceTransformer
        _model_cache[model_name] = SentenceTransformer(model_name)
    return _model_cache[model_name]


def batch_embed_local(texts: list, model_name: str = "all-MiniLM-L6-v2", show_progress: bool = False) -> np.ndarray:
    """Embed a list of texts using the local model. Returns (n, dim) array."""
    model = get_local_model(model_name)
    arr = model.encode(texts, convert_to_numpy=True, show_progress_bar=show_progress)
    return np.asarray(arr)


def batch_cosine_similarity(query_vec: np.ndarray, matrix: np.ndarray) -> np.ndarray:
    """Compute cosine similarity between query_vec and each row of matrix. Returns 1d array."""
    query_vec = np.asarray(query_vec, dtype=np.float64).ravel()
    matrix = np.asarray(matrix, dtype=np.float64)
    if query_vec.ndim == 1:
        query_vec = query_vec.reshape(1, -1)
    dots = np.dot(matrix, query_vec.T).ravel()
    norms_q = np.linalg.norm(query_vec)
    norms_m = np.linalg.norm(matrix, axis=1)
    norms_m = np.where(norms_m == 0, 1e-10, norms_m)
    return (dots / (norms_q * norms_m)).ravel()


def normalize_scores(scores: np.ndarray) -> np.ndarray:
    """Min-max normalize scores to [0, 1]. Handles constant arrays."""
    scores = np.asarray(scores, dtype=np.float64)
    min_s, max_s = scores.min(), scores.max()
    if max_s - min_s <= 1e-12:
        return np.ones_like(scores) if max_s > 0 else np.zeros_like(scores)
    return (scores - min_s) / (max_s - min_s)
