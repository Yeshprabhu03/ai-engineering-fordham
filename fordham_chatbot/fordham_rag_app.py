import streamlit as st
import pandas as pd
import os
import zipfile
import pathlib
import numpy as np
from sentence_transformers import SentenceTransformer
import openai
from dotenv import load_dotenv

load_dotenv()

# Page Config
st.set_page_config(page_title="Fordham RAG", layout="wide")

# --- 1. Data Loading (Optimized) ---
@st.cache_resource
def load_cached_data():
    return pd.read_pickle('data/processed_fordham.pkl')

# --- 2. Model Loading (Simplified) ---
# We don't need to load a heavy model anymore, just use OpenAI client

# --- Main App Logic ---

# --- Main App Logic ---

# --- Main App Logic ---

# Check/Load Logo
# Logo URL
logo_src = "https://www.fordham.edu/images/Fordham_University_Logo_Maroon_RGB.png"

# Custom CSS for Fordham Theme
# Custom CSS for "Oat" Theme (Minimalist)
st.markdown(f"""
<style>
    /* Remove default Streamlit top padding */
    .stApp > header {{
        display: none;
    }}
    .main .block-container {{
        padding-top: 2rem;
        padding-bottom: 2rem;
    }}
    
    /* Global Styles - Oat/Paper Aesthetic */
    .stApp {{
        background-color: #FBFBF8;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        color: #2A2A2A;
    }}
    
    /* Typography */
    h1, h2, h3 {{
        font-family: 'Georgia', serif;
        color: #1A1A1A;
        font-weight: 600;
    }}
    
    /* Custom Header styling - Minimal */
    .fordham-header-minimal {{
        text-align: center;
        padding: 20px 0 40px 0;
        border-bottom: 1px solid #E6E6E6;
        margin-bottom: 30px;
    }}
    .fordham-shield-icon {{
        max-width: 300px;
        width: 100%;
        height: auto;
        margin-bottom: 10px;
    }}
    .fordham-title {{
        font-family: 'Georgia', serif;
        font-size: 28px;
        color: #860038; /* Fordham Maroon Accent */
        letter-spacing: 1px;
        margin: 0;
    }}
    .fordham-subtitle {{
        font-family: 'Inter', sans-serif;
        font-size: 14px;
        color: #666;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-top: 5px;
    }}

    /* Chat Styling - Clean & distinct */
    .stChatMessage {{
        background-color: transparent;
        border: none;
        padding: 15px 0;
        border-bottom: 1px solid #F0F0F0;
    }}
    div[data-testid="stChatMessageContent"] {{
        font-family: 'Inter', sans-serif;
        line-height: 1.6;
        color: #333;
    }}
    
    /* User Message Specific (if targeting is possible, otherwise general) */
    .stChatMessage[data-testid="stChatMessage"]:nth-child(even) {{
        background-color: #F5F5F5; /* Slight gray for contrast if needed, or keep transparent */
    }}
    
    /* Input Field - Clean border, no shadow */
    .stTextInput > div > div > input {{
        background-color: #FFFFFF;
        border: 1px solid #E0E0E0;
        border-radius: 8px;
        color: #333;
        font-family: 'Inter', sans-serif;
        box-shadow: none;
    }}
    .stTextInput > div > div > input:focus {{
        border-color: #860038;
        box-shadow: 0 0 0 1px #860038;
    }}
    
    /* Button Styling - Minimal Accent */
    .stButton>button {{
        background-color: #860038;
        color: white;
        border-radius: 6px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: 500;
        transition: all 0.2s ease;
    }}
    .stButton>button:hover {{
        background-color: #a00043;
        transform: translateY(-1px);
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }}
</style>

<!-- Minimal Header HTML -->
<div class="fordham-header-minimal">
    <img src="{logo_src}" class="fordham-shield-icon" alt="Fordham Logo">
    <div class="fordham-subtitle">AI Assistant</div>
</div>
""", unsafe_allow_html=True)

# --- 1. Data Loading & Preparation ---
@st.cache_resource
def load_data():
    # Paths (Relative to this script)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    corpus_path = os.path.join(current_dir, 'data', 'corpus.pkl')
    embeddings_path = os.path.join(current_dir, 'data', 'embeddings.npy')
    
    if os.path.exists(corpus_path) and os.path.exists(embeddings_path):
        with st.spinner("Loading data..."):
            df = pd.read_pickle(corpus_path)
            embeddings = np.load(embeddings_path)
            return df, embeddings
    else:
        st.error(f"Data files not found at {corpus_path}! Please run `prepare_data.py` locally to generate data.")
        st.stop()
        return None, None

# Load Data
df_chunks, embeddings_array = load_data()

# Robustness check: Ensure length match
if len(df_chunks) != len(embeddings_array):
    st.error(f"Data Mismatch! Corpus has {len(df_chunks)} rows but embeddings has {len(embeddings_array)} rows. Please regenerate data.")
    st.stop()

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat Input
if prompt := st.chat_input("Ask a question about Fordham..."):
    # Check API Key
    if not os.environ.get("OPENAI_API_KEY"):
         st.error("OpenAI API Key not found! Please check your .env file.")
         st.stop()
         
    # Display user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate Response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            client = openai.OpenAI()
            
            # 1. Retrieve
            with st.spinner("Searching Fordham's knowledge base..."):
                response = client.embeddings.create(input=prompt, model="text-embedding-3-small")
                query_embedding = response.data[0].embedding
            
                # Stack embeddings (Now it is already a numpy array)
                embeddings = embeddings_array
                
                # Normalize
                query_norm = query_embedding / np.linalg.norm(query_embedding)
                # embeddings is already a numpy array from load_data
                embeddings_norm = embeddings / np.linalg.norm(embeddings, axis=1)[:, np.newaxis]
                
                # Dot product
                scores = np.dot(embeddings_norm, query_norm)
                
                # Top K
                top_k = 5
                top_k_indices = np.argsort(scores)[::-1][:top_k]
                results = df_chunks.iloc[top_k_indices]
                
                # Context
                context_list = []
                for i, row in results.iterrows():
                    fname = row.get('filename', 'unknown')
                    url = row.get('url', '#')
                    context_list.append(f"SOURCE: {fname} ({url})\nCONTENT: {row['content']}")
                context_block = "\n\n---\n\n".join(context_list)
            
            # 2. Answer
            system_message = (
                "You are the Fordham University AI Assistant (RamBot). "
                "Answer the user's question concisely using the provided context. "
                "Always cite your sources if possible. "
                "If the context doesn't contain the answer, say you don't know."
            )
            
            # Construct messages with history
            messages = [{"role": "system", "content": system_message}]
            
            # Add last few exchanges for context (optional, but good for "it", "they")
            # We limit this to avoid hitting token limits with strict RAG context
            for m in st.session_state.messages[-4:]: 
                messages.append({"role": m["role"], "content": m["content"]})
            
            # Add current RAG context and question
            # We treat the context as a system/user injection for the current turn
            messages.append({"role": "user", "content": f"Context:\n{context_block}\n\nQuestion: {prompt}"})
            
            chat_completion = client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                stream=True
            )
            
            # Stream response
            for chunk in chat_completion:
                if chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
                    message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
            
            # Append sources accordion
            with st.expander("View Sources"):
                for i, row in results.iterrows():
                    st.markdown(f"**[{row['filename']}]({row['url']})**")
                    st.caption(row['content'][:200] + "...")

            # Add to history
            # Only add the text response to history to keep it clean for context
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"Error: {e}")
