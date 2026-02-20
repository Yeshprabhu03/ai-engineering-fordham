import asyncio
import litellm
import textwrap
import pandas as pd
from pydantic import BaseModel, Field

# Ensure litellm is installed
# !uv pip install litellm

class HallucinationEval(BaseModel):
    chain_of_thought: str = Field(description="Step-by-step reasoning about whether the answer is supported by the context")
    is_supported: bool = Field(description="True if the answer is FULLY supported by the context without introducing outside facts. False otherwise.")

async def evaluate_hallucination(question: str, generated_answer: str, context: str) -> dict:
    """Uses an LLM as a judge to evaluate if the generated answer hallucinates."""
    try:
        response = await litellm.acompletion(
            model="gpt-4o",  # Using a stronger model for evaluation
            messages=[
                {
                    "role": "user",
                    "content": textwrap.dedent(f"""
                    You are an expert evaluator for an AI application.
                    You will be given a QUESTION, a retrieved CONTEXT, and a GENERATED ANSWER.
                    
                    Your job is to determine if the GENERATED ANSWER is fully supported by the CONTEXT.
                    - If the answer includes facts not found in the context, it is a hallucination (is_supported = False).
                    - If the answer correctly says "I don't know" when the context lacks information, that is NOT a hallucination (is_supported = True).
                    - If the answer accurately summarizes the context to answer the question, it is supported (is_supported = True).
                    
                    [QUESTION]
                    {question}
                    
                    [CONTEXT]
                    {context}
                    
                    [GENERATED ANSWER]
                    {generated_answer}
                    """
                    ),
                }
            ],
            response_format=HallucinationEval,
        )
        
        result = HallucinationEval.model_validate_json(response.choices[0].message.content)
        return {"question": question, "is_supported": result.is_supported, "reasoning": result.chain_of_thought}
    except Exception as e:
        print(f"Error evaluating hallucination: {e}")
        return None

if 'synthetic_df' in globals() and 'retrieve_hybrid' in globals() and 'generate_answer' in globals():
    eval_rows = []
    
    print(f"Evaluating Generation (Hallucination check) for {min(20, len(synthetic_df))} questions...")
    # Sample a smaller subset to save time/API costs
    sample_to_eval = synthetic_df.sample(min(20, len(synthetic_df)), random_state=42)
    
    # 1. First, generate answers using our RAG pipeline
    rag_results = []
    for _, row in sample_to_eval.iterrows():
        question = row["question"]
        
        # Retrieve context (Using Hybrid for best results)
        retrieved_df = retrieve_hybrid(question, df_chunks, top_k=5, alpha=0.5)
        
        # Build context string exactly as generate_answer does
        context_list = [f"SOURCE: {r.get('filename', r.get('parent_file', 'unknown'))}\\nCONTENT: {r['content']}" for _, r in retrieved_df.iterrows()]
        context_block = "\\n\\n---\\n\\n".join(context_list)
        
        # Generate the final RAG answer
        # Note: we pass df_chunks, but the internal generate_answer function might use standard retrieve().
        # To be strict, we'll just use the existing generate_answer function for testing black-box end-to-end.
        generated_ans = generate_answer(question, df_chunks) 
        
        rag_results.append({
            "question": question,
            "generated_answer": generated_ans,
            "context_used": context_block
        })
        
    print("Answers generated. Now running LLM-as-a-judge evaluation...")
    
    # 2. Evaluate those answers concurrently
    tasks = [evaluate_hallucination(r["question"], r["generated_answer"], r["context_used"]) for r in rag_results]
    
    # Needs to be run inside an async event loop, usually Jupyter handles this automatically
    import nest_asyncio
    nest_asyncio.apply()
    
    async def run_evals():
        return await asyncio.gather(*tasks)
        
    hallucination_results = asyncio.run(run_evals())
    hallucination_results = [r for r in hallucination_results if r is not None]
    
    # 3. Analyze Results
    hallucination_df = pd.DataFrame(hallucination_results)
    fidelity_score = hallucination_df["is_supported"].mean()
    
    print("\\n--- Generation Evaluation Results ---\\n")
    print(f"Fidelity Score (Answers fully supported by context without hallucination): {fidelity_score * 100:.1f}%\\n")
    
    # Show examples of hallucinations if any exist
    hallucinations = hallucination_df[~hallucination_df["is_supported"]]
    if len(hallucinations) > 0:
        print("Examples of Hallucinations:")
        for _, row in hallucinations.head(3).iterrows():
            print(f"- Q: {row['question']}")
            print(f"  Reasoning: {row['reasoning']}\\n")
    else:
        print("No hallucinations detected in this sample! Excellent.")

else:
    print("Please make sure synthetic_df and your RAG functions are defined first!")
