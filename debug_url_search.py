import pandas as pd
import os

# Set up paths
base_dir = "fordham_chatbot"
corpus_path = os.path.join(base_dir, "data", "corpus.pkl")

# Load existing corpus
print(f"Loading corpus from {corpus_path}...")
df = pd.read_pickle(corpus_path)

# Search
search_term = "tuition-and-payments/graduate-tuition/gabelli-school-of-business"
results = df[df['url'].str.contains(search_term, case=False, na=False)]

print(f"Found {len(results)} matches for URL containing '{search_term}'")

if not results.empty:
    print("\nExample content:")
    print(results.iloc[0]['content'][:500])
else:
    # Try broader
    print("\nTrying broader search for 'graduate-tuition'...")
    search_term_2 = "graduate-tuition"
    results_2 = df[df['url'].str.contains(search_term_2, case=False, na=False)]
    print(f"Found {len(results_2)} matches for URL containing '{search_term_2}'")
    if not results_2.empty:
        print("\nExample URLs:")
        print(results_2['url'].head().to_list())
