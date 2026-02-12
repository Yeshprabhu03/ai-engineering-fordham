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

# --- 1. Data Loading & Preparation ---
@st.cache_resource
def load_data():
    # Path to pre-computed data
    data_path = 'data/processed_fordham.pkl'
    
    if os.path.exists(data_path):
        return pd.read_pickle(data_path)
    
    # If not found, generate it!
    st.warning("Pre-computed data not found. Generating embeddings... This may take a minute.")
    
    # Check for source zip
    zip_path = 'data/fordham-website.zip'
    source_dir = 'data/fordham-website'
    
    # Unzip if needed
    if not os.path.exists(source_dir):
        if os.path.exists(zip_path):
            with st.spinner("Unzipping source data..."):
                with zipfile.ZipFile(zip_path, 'r') as z:
                    z.extractall(".")
        else:
            st.error(f"Source data not found! Please ensure '{zip_path}' exists in the repo.")
            st.stop()
            
    # Load raw markdown files
    data = []
    with st.spinner("Loading markdown files..."):
        # Walk through directory
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                if file.endswith(".md"):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            lines = f.readlines()
                            if not lines: continue
                            url = lines[0].strip()
                            content = "".join(lines[1:]).strip()
                            data.append({
                                "filename": file,
                                "url": url,
                                "content": content
                            })
                    except Exception:
                        continue
                        
    df = pd.DataFrame(data)
    
    # Chunking function
    def chunk_text(text, chunk_size=800, overlap=150):
        chunks = []
        if not text: return chunks
        start = 0
        text_len = len(text)
        while start < text_len:
            end = start + chunk_size
            chunk = text[start:end]
            chunks.append(chunk)
            step = chunk_size - overlap
            if step <= 0: step = 1
            start += step
        return chunks

    # Chunking
    chunked_data = []
    with st.spinner(f"Chunking {len(df)} documents..."):
        for index, row in df.iterrows():
            content = row.get('content', '')
            if not isinstance(content, str): content = ""
            text_chunks = chunk_text(content)
            for i, chunk_content in enumerate(text_chunks):
                if not chunk_content.strip(): continue
                chunked_data.append({
                    "chunk_id": f"{row['filename']}_{i}",
                    "source_url": row['url'],
                    "content": chunk_content.strip(),
                    "filename": row['filename'],
                    "url": row['url'] # Redundant but safe
                })
    
    df_chunks = pd.DataFrame(chunked_data)
    
    # Embeddings
    if not os.environ.get("OPENAI_API_KEY"):
        st.error("OpenAI API Key needed for data generation!")
        st.stop()
        
    client = openai.OpenAI()
    
    # Batch processing
    batch_size = 100 # Safe for OpenAI
    embeddings = []
    
    progress_bar = st.progress(0)
    total_chunks = len(df_chunks)
    
    for i in range(0, total_chunks, batch_size):
        batch = df_chunks.iloc[i:i+batch_size]['content'].tolist()
        try:
            response = client.embeddings.create(input=batch, model="text-embedding-3-small")
            batch_embeddings = [data.embedding for data in response.data]
            embeddings.extend(batch_embeddings)
            
            # Update progress
            progress = min(1.0, (i + batch_size) / total_chunks)
            progress_bar.progress(progress)
            
        except Exception as e:
            st.error(f"Error generating embeddings: {e}")
            st.stop()
            
    df_chunks['embedding'] = embeddings
    
    # Save for next time
    df_chunks.to_pickle(data_path)
    
    st.success("Data generation complete! Reloading...")
    return df_chunks

# Load Data
df_chunks = load_data()

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
