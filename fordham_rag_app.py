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
st.title("Fordham University AI Assistant 🐏")

st.markdown("**Your personal AI guide to everything Fordham.** Ask me anything!")

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
logo_src = "https://upload.wikimedia.org/wikipedia/commons/c/c5/Fordham_University_Seal.svg"

# Custom CSS for Fordham Theme
st.markdown(f"""
<style>
    /* Remove default Streamlit top padding */
    .stApp > header {{
        display: none;
    }}
    .main .block-container {{
        padding-top: 0;
        margin-top: 0;
    }}
    
    /* Global Styles */
    .stApp {{
        background-color: #FFFFFF;
        font-family: 'Georgia', serif;
    }}
    
    /* Custom Header styling */
    .fordham-header {{
        background-color: #860038;
        padding: 40px 20px;
        text-align: center;
        border-bottom: 5px solid #b20e3e;
        margin-bottom: 30px;
    }}
    .fordham-logo-text {{
        color: white;
        font-family: 'Georgia', serif;
        font-size: 42px;
        font-weight: bold;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin: 0;
    }}
    /* Removed Subtext */
    
    /* Top thin bar */
    .top-bar {{
        background-color: #4a001f;
        height: 10px;
        width: 100%;
    }}

    /* Chat Styling */
    .stChatMessage {{
        border-radius: 10px;
        padding: 10px;
        border: 1px solid #eee;
    }}
    div[data-testid="stChatMessageContent"] {{
        font-family: 'Arial', sans-serif;
    }}
    
    /* Button Styling */
    .stButton>button {{
        background-color: #860038;
        color: white;
        border-radius: 5px;
        border: none;
    }}
    .stButton>button:hover {{
        background-color: #a00043;
        color: white;
    }}
</style>

<!-- Custom Header HTML -->
<div class="top-bar"></div>
<div class="fordham-header">
<div style="display: flex; justify-content: center; align-items: center; gap: 20px;">
<!-- Inline SVG Logo -->
<svg width="400" height="80" viewBox="0 0 400 80" xmlns="http://www.w3.org/2000/svg">
<!-- Shield Group -->
<g transform="translate(10, 5)">
<!-- Shield Shape -->
<path d="M 5 5 L 65 5 L 65 25 C 65 60 35 75 35 75 C 35 75 5 60 5 25 Z" fill="#860038" stroke="white" stroke-width="2"/>
<!-- The 'F' -->
<text x="35" y="55" font-family="'Times New Roman', serif" font-weight="bold" font-size="50" fill="white" text-anchor="middle">F</text>
</g>
<!-- University Text -->
<text x="80" y="52" font-family="'Georgia', serif" font-weight="bold" font-size="34" fill="white" letter-spacing="2">FORDHAM</text>
<text x="80" y="75" font-family="'Arial', sans-serif" font-weight="bold" font-size="14" fill="white" letter-spacing="4">UNIVERSITY</text>
</svg>
</div>
</div>
""", unsafe_allow_html=True)

# Load Data
if os.path.exists('data/processed_fordham.pkl'):
    # Optimize loading time by skipping spinner if already in memory (Streamlit cache handles this, but UI effect is good)
    # We'll just load it quietly
    df_chunks = load_cached_data()
else:
    st.error("Pre-computed data not found! Please run 'python3 prepare_data.py' to generate 'data/processed_fordham.pkl'.")
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
            
                # Stack embeddings
                embeddings = np.stack(df_chunks['embedding'].values)
                
                # Normalize
                query_norm = query_embedding / np.linalg.norm(query_embedding)
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
            user_message = f"Context:\n{context_block}\n\nQuestion: {prompt}"
            
            chat_completion = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_message}
                ],
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
