import json

path = '/Users/yeshwanth/Desktop/ai-engineering-fordham/5.you-can-just-build-things.ipynb'
with open(path, 'r') as f:
    nb = json.load(f)

insert_index = -1
for i, cell in enumerate(nb.get('cells', [])):
    if cell.get('cell_type') == 'code' and any('import matplotlib.pyplot as plt' in line for line in cell.get('source', [])):
        insert_index = i
        break

if insert_index != -1:
    markdown_cell = {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### Evaluation Analysis\n",
            "\n",
            "**1. BM25 (Full Text Search / Lexical)**\n",
            "- Performs well when exact keyword matches are present in the text (e.g., specific names, course IDs, or strict terminology).\n",
            "- Often struggles with semantic understanding. If the user asks a question using synonyms rather than the exact wording from the document, recall and precision drop significantly (i.e. vocabulary mismatch problem).\n",
            "\n",
            "**2. Custom Vector Search (Semantic)**\n",
            "- Captures the underlying meaning of the question rather than just surface-level keywords.\n",
            "- Better at handling paraphrased questions, typos, and variations in how a prospective student might frame a question.\n",
            "- However, it can sometimes retrieve documents that are semantically close but fundamentally incorrect (e.g., retrieving a page about 'Computer Science faculty' when asked about 'Computer Science tuition').\n",
            "\n",
            "**3. Hybrid Search (Vector + BM25)**\n",
            "- Combines the strengths of both approaches by weighting the semantic relevance and the keyword match relevance (using our `alpha=0.5` parameter).\n",
            "- As seen in the graphs, it noticeably improves overall **Recall@k** and stabilizes **Precision@k**. It ensures that documents with exact keyword matches are boosted, while still maintaining high recall for semantically related documents.\n",
            "- This approach represents the best of both worlds, which is why modern enterprise RAG systems typically utilize a Hybrid retrieval strategy out of the box."
        ]
    }
    
    nb['cells'].insert(insert_index + 1, markdown_cell)
    
    with open(path, 'w') as f:
        json.dump(nb, f, indent=1)
    print("Added markdown cell successfully.")
else:
    print("Could not find the plotting cell.")
