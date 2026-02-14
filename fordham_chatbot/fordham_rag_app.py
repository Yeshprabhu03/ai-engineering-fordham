print(">>> SCRIPT LOADING: Starting imports...")
import streamlit as st
import pandas as pd
import os
import zipfile
import pathlib
import numpy as np
# from sentence_transformers import SentenceTransformer (Unused, removed to speed up build)
import openai
from dotenv import load_dotenv

load_dotenv()

# Page Config
st.set_page_config(page_title="Fordham RAG", layout="wide")
print(">>> APP START: Page config set")

# --- Main App Logic ---

# Check/Load Logo
# Paths (Relative to this script)
current_dir = os.path.dirname(os.path.abspath(__file__))
logo_path = os.path.join(current_dir, 'data', 'fordham_logo.svg')

# Custom CSS for Fordham Theme
st.markdown(f"""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Lato:wght@400;700&family=Playfair+Display:wght@600;700&display=swap');

    /* Remove default Streamlit top padding */
    .stApp > header {{
        display: none;
    }}
    .main .block-container {{
        padding-top: 2rem;
        padding-bottom: 2rem;
    }}
    
    /* Global Styles */
    .stApp {{
        background-color: #FBFBF8;
        font-family: 'Lato', sans-serif;
        color: #2A2A2A;
    }}
    
    /* Typography */
    h1, h2, h3 {{
        font-family: 'Playfair Display', serif;
        color: #860038; /* Fordham Maroon */
        font-weight: 700;
    }}
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {{
        background-color: #F5F5F5;
        border-right: 1px solid #E0E0E0;
    }}
    
    /* Chat Styling */
    .stChatMessage {{
        background-color: transparent;
        border: none;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }}
    
    /* User Message */
    .stChatMessage[data-testid="stChatMessage"]:nth-child(odd) {{
        background-color: #ffffff;
        border: 1px solid #E0E0E0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }}
    
    /* Assistant Message */
    .stChatMessage[data-testid="stChatMessage"]:nth-child(even) {{
        background-color: #F9F9F9;
        border: 1px solid #F0F0F0;
    }}

    /* Input Field */
    .stTextInput > div > div > input {{
        background-color: #FFFFFF;
        border: 1px solid #E0E0E0;
        border-radius: 8px;
        color: #333;
        font-family: 'Lato', sans-serif;
        box-shadow: none;
    }}
    .stTextInput > div > div > input:focus {{
        border-color: #860038;
        box-shadow: 0 0 0 1px #860038;
    }}
    
    /* Buttons */
    .stButton>button {{
        background-color: #860038;
        color: white;
        border-radius: 6px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: 600;
        font-family: 'Lato', sans-serif;
        transition: all 0.2s ease;
        width: 100%;
    }}
    .stButton>button:hover {{
        background-color: #a00043;
        transform: translateY(-1px);
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }}
</style>
""", unsafe_allow_html=True)

# Sidebar Layout
with st.sidebar:
    # Logo
    if os.path.exists(logo_path):
        st.image(logo_path, width=120)
    
    st.markdown("### Fordham AI Assistant")
    
    # Model Selection (Cost Optimization)
    model = st.selectbox(
        "Model", 
        ["gpt-4o-mini", "gpt-4o"], 
        index=0,
        help="gpt-4o-mini is faster and cheaper. Use gpt-4o for complex reasoning."
    )
    
    st.markdown("---")
    
    st.markdown("""
    **About**
    
    This AI assistant uses RAG (Retrieval-Augmented Generation) to answer questions about Fordham University using official documentation.
    
    **Features:**
    - 📚 Knowledge from ~49k documents
    - 🧠 Context-aware conversations
    - 🔗 Source citations
    """)
    
    st.markdown("---")

    # Clear Chat Button
    if st.button("Clear Conversation", type="primary"):
        st.session_state.messages = []
        st.rerun()

# Main Header
st.title("Fordham University AI Assistant")
st.markdown("Ask anything about Fordham's programs, faculty, or campus life.")
st.markdown("---")

# --- 1. Data Loading & Preparation ---
@st.cache_resource
def load_data():
    # Paths (Relative to this script)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    corpus_path = os.path.join(current_dir, 'data', 'corpus.pkl')
    embeddings_path = os.path.join(current_dir, 'data', 'embeddings.npy')
    
    if os.path.exists(corpus_path) and os.path.exists(embeddings_path):
        print(f">>> DATA LOADING: Found files. Starting read...")
        with st.spinner("Loading data..."):
            df = pd.read_pickle(corpus_path)
            print(f">>> DATA LOADING: Corpus loaded ({len(df)} rows)")
            embeddings = np.load(embeddings_path)
            print(f">>> DATA LOADING: Embeddings loaded ({embeddings.shape})")
            return df, embeddings
    else:
        st.error(f"Data files not found at {corpus_path}! Please run `prepare_data.py` locally to generate data.")
        st.stop()
        return None, None

# Load Data
df_chunks, embeddings_array = load_data()
print(">>> DATA LOADING: Complete")

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
prompt = st.chat_input("Ask a question about Fordham...")

if prompt:
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
                model=model,
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
