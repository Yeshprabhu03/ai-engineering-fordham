import json

notebook_path = "/Users/yeshwanth/Desktop/ai-engineering-fordham/5.you-can-just-build-things.ipynb"

# Load notebook
with open(notebook_path, "r", encoding="utf-8") as f:
    nb = json.load(f)

# The new cells we want to add
new_cells = [
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### Synthetic Question Generation (Evaluation)\\n",
            "Since we don't have human-labeled ground truth for the Fordham dataset, we can generate **synthetic questions** using an LLM to test our system, just like we did with the nfcorpus dataset!\\n",
            "\\n",
            "Let's sample some chunks from `df_chunks` and create a test set."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "import pandas as pd\\n",
            "import litellm\\n",
            "import asyncio\\n",
            "import random\\n",
            "import textwrap\\n",
            "from pydantic import BaseModel, Field\\n",
            "\\n",
            "# Ensure litellm is installed\\n",
            "# !uv pip install litellm\\n",
            "\\n",
            "class SyntheticQuestion(BaseModel):\\n",
            "    chain_of_thought: str = Field(description=\"Step-by-step reasoning about what makes a good question for this document\")\\n",
            "    question: str = Field(description=\"A natural, specific question that can be answered using the document\")\\n",
            "    answer: str = Field(description=\"The answer to the question\")\\n",
            "\\n",
            "constraints = [\\n",
            "    \"The question should be answerable in one word or a short phrase\",\\n",
            "    \"The question should require synthesizing multiple facts from the document\",\\n",
            "    \"Frame the question as something a prospective student might ask\",\\n",
            "    \"Ask about a specific group, deadline, or requirement mentioned in the document\",\\n",
            "]\\n",
            "\\n",
            "async def generate_question(doc_id: str, content: str) -> dict:\\n",
            "    \"\"\"Generate a synthetic question for a single chunk using an LLM.\"\"\"\\n",
            "    constraint = random.choice(constraints)\\n",
            "    try:\\n",
            "        # Make sure OPENAI_API_KEY is set in your environment variables!\\n",
            "        response = await litellm.acompletion(\\n",
            "            model=\"gpt-4o-mini\",\\n",
            "            messages=[\\n",
            "                {\\n",
            "                    \"role\": \"user\",\\n",
            "                    \"content\": textwrap.dedent(f\"\"\"\\n",
            "                    I will give you a document chunk from the Fordham University website. Please generate a question that can be answered using the following document.\\n",
            "                    \\n",
            "                    Text: {content}\\n",
            "                    \\n",
            "                    Rules:\\n",
            "                    - Your question should be natural and specific and concise\\n",
            "                    - Your question should not assume that someone is reading the document, but rather that they are asking a general question about Fordham\\n",
            "                    - Your question must be answerable using the document that I gave you\\n",
            "                    - {constraint}\\n",
            "                    - Do not reference \"the document\" or \"the webpage\" in your question\\n",
            "                    \"\"\"\\n",
            "                    ),\\n",
            "                }\\n",
            "            ],\\n",
            "            response_format=SyntheticQuestion,\\n",
            "        )\\n",
            "        \\n",
            "        result = SyntheticQuestion.model_validate_json(response.choices[0].message.content)\\n",
            "        return {\"doc_id\": doc_id, \"question\": result.question, \"answer\": result.answer}\\n",
            "    except Exception as e:\\n",
            "        print(f\"Error generating question: {e}\")\\n",
            "        return None\\n",
            "\\n",
            "# Sample 40 chunks to evaluate on\\n",
            "if 'df_chunks' in globals():\\n",
            "    sample_docs = df_chunks.dropna(subset=['content']).sample(n=40, random_state=42)\\n",
            "    \\n",
            "    # Generate all questions concurrently\\n",
            "    print(f\"Generating {len(sample_docs)} synthetic questions...\")\\n",
            "    tasks = [generate_question(row[\"chunk_id\"], row[\"content\"]) for _, row in sample_docs.iterrows()]\\n",
            "    \\n",
            "    # Run the async loop\\n",
            "    synthetic_results = await asyncio.gather(*tasks)\\n",
            "    \\n",
            "    # Filter out failed generations\\n",
            "    synthetic_results = [r for r in synthetic_results if r is not None]\\n",
            "    \\n",
            "    synthetic_df = pd.DataFrame(synthetic_results)\\n",
            "    print(f\"Generated {len(synthetic_df)} synthetic questions\\\\n\")\\n",
            "    \\n",
            "    # Show some examples\\n",
            "    for _, row in synthetic_df.head(3).iterrows():\\n",
            "        doc = df_chunks[df_chunks[\"chunk_id\"] == row[\"doc_id\"]].iloc[0]\\n",
            "        print(f\"Q: {row['question']}\")\\n",
            "        print(f\"   Source Chunk: {doc['content'][:80]}...\")\\n",
            "        print(f\"   Answer: {row['answer']}\")\\n",
            "        print()\\n",
            "else:\\n",
            "    print(\"Please run the earlier cells to create df_chunks first!\")"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### Run Retrieval Evaluation\\n",
            "We will now run our vector search `retrieve()` function (from Section 4) on these 40 questions to see how well it fetches the ground-truth chunk!"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "if 'synthetic_df' in globals() and 'retrieve' in globals():\\n",
            "    syn_rows = []\\n",
            "    \\n",
            "    k_values = [1, 3, 5, 10]\\n",
            "    max_k = max(k_values)\\n",
            "    \\n",
            "    print(f\"Evaluating retrieval for {len(synthetic_df)} questions...\")\\n",
            "    \\n",
            "    for _, row in synthetic_df.iterrows():\\n",
            "        source_id = row[\"doc_id\"]\\n",
            "        question = row[\"question\"]\\n",
            "    \\n",
            "        # Search using custom retrieve function\\n",
            "        try:\\n",
            "            retrieved_df = retrieve(question, df_chunks, top_k=max_k)\\n",
            "            retrieved_ids = retrieved_df['chunk_id'].tolist()\\n",
            "        except Exception as e:\\n",
            "            print(f\"Error retrieving: {e}\")\\n",
            "            continue\\n",
            "    \\n",
            "        for k in k_values:\\n",
            "            ids_at_k = retrieved_ids[:k]\\n",
            "    \\n",
            "            # Binary relevance (we only have 1 true relevant chunk per synthetic question)\\n",
            "            found = source_id in ids_at_k\\n",
            "            precision = (1.0 if found else 0.0) / k  \\n",
            "            recall = 1.0 if found else 0.0  \\n",
            "    \\n",
            "            syn_rows.append({\"metric\": \"precision\", \"k\": k, \"score\": precision, \"question\": question})\\n",
            "            syn_rows.append({\"metric\": \"recall\", \"k\": k, \"score\": recall, \"question\": question})\\n",
            "    \\n",
            "    syn_eval_df = pd.DataFrame(syn_rows)\\n",
            "    \\n",
            "    print(\"\\\\n--- Synthetic Evaluation Results (Custom Vector Search) ---\\\\n\")\\n",
            "    print(syn_eval_df.groupby([\"metric\", \"k\"])[\"score\"].mean().round(4).to_string())\\n",
            "else:\\n",
            "    print(\"Please generate synthetic_df first!\")"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### Plot the Results"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "import matplotlib.pyplot as plt\\n",
            "\\n",
            "if 'syn_eval_df' in globals():\\n",
            "    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))\\n",
            "    \\n",
            "    data_p = syn_eval_df[syn_eval_df[\"metric\"] == \"precision\"]\\n",
            "    means_p = data_p.groupby(\"k\")[\"score\"].mean()\\n",
            "    ax1.plot(means_p.index, means_p.values, marker=\"o\", color='tab:blue')\\n",
            "    ax1.set_xlabel(\"k\")\\n",
            "    ax1.set_ylabel(\"Precision@k\")\\n",
            "    ax1.set_title(\"Precision@k for Custom Vector Search\")\\n",
            "    ax1.grid(True)\\n",
            "    ax1.set_ylim(0, 1.05)\\n",
            "    \\n",
            "    data_r = syn_eval_df[syn_eval_df[\"metric\"] == \"recall\"]\\n",
            "    means_r = data_r.groupby(\"k\")[\"score\"].mean()\\n",
            "    ax2.plot(means_r.index, means_r.values, marker=\"o\", color='tab:orange')\\n",
            "    ax2.set_xlabel(\"k\")\\n",
            "    ax2.set_ylabel(\"Recall@k\")\\n",
            "    ax2.set_title(\"Recall@k for Custom Vector Search\")\\n",
            "    ax2.grid(True)\\n",
            "    ax2.set_ylim(0, 1.05)\\n",
            "    \\n",
            "    plt.tight_layout()\\n",
            "    plt.show()"
        ]
    }
]

# Find where to insert (after section 8 marker or placeholder)
insert_idx = len(nb["cells"])

for i, cell in enumerate(nb["cells"]):
    if cell["cell_type"] == "markdown":
        if any("8. (Optional) Make it an app" in line for line in cell["source"]):
            insert_idx = i
            break

# Also, there's a placeholder empty code cell. We can just insert right before the next markdown section.
nb["cells"] = nb["cells"][:insert_idx] + new_cells + nb["cells"][insert_idx:]

with open(notebook_path, "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=1)

print("Injected new cells into the notebook successfully.")
