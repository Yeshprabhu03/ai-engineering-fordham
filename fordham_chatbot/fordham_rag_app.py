print(">>> SCRIPT LOADING: Starting imports...")
import streamlit as st
import pandas as pd
import os
import zipfile
import pathlib
import numpy as np
# from sentence_transformers import SentenceTransformer (Unused, removed to speed up build)
import openai
from audio_recorder_streamlit import audio_recorder
from dotenv import load_dotenv

load_dotenv()

# Page Config
st.set_page_config(page_title="Fordham RAG", layout="wide", initial_sidebar_state="collapsed")
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
    /* Floating Microphone Hack */
    /* Target the container holding the audio recorder */
    div.element-container:has(iframe[title="audio_recorder_streamlit.audio_recorder"]) {{
        position: fixed;
        bottom: 45px; /* Moved up to be inside the input bar */
        right: 55px;  /* Left of the send button */
        z-index: 999999; /* Ensure it's on top of everything */
        width: auto !important;
        height: 0px !important; /* Collapse ghost space */
        margin: 0px !important;
        overflow: visible !important;
    }}
    
    /* Make the iframe itself visible despite container height 0 */
    iframe[title="audio_recorder_streamlit.audio_recorder"] {{
        height: 50px !important; /* Slightly smaller to fit nicely */
        width: 50px !important;
    }}
</style>
""", unsafe_allow_html=True)

# Clear Chat Button
if st.button("Clear Conversation", type="primary"):
    st.session_state.messages = []
    st.rerun()

# Sidebar Layout (Removed)
# with st.sidebar:
#     ... (Removed)

# Model Selection (Hidden/Hardcoded)
model = "gpt-4o-mini"

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
# Handle both text input and voice input

# Place microphone just before chat input
# The CSS above handles the positioning, so we just render it here
audio_bytes = audio_recorder(
    text="",
    recording_color="#e8b62c",
    neutral_color="#6aa36f",
    icon_name="microphone",
    icon_size="1x", # Smaller icon to fit the bar
    pause_threshold=2.0,
    key="voice_input_fixed" # Unique key to prevent re-render loss
)

voice_prompt = None
if audio_bytes:
    with st.spinner("Transcribing..."):
        try:
            # Save to temp file
            temp_audio_path = "temp_audio.mp3"
            with open(temp_audio_path, "wb") as f:
                f.write(audio_bytes)
            
            # Transcribe with Whisper
            client = openai.OpenAI()
            with open(temp_audio_path, "rb") as audio_file:
                transcript = client.audio.transcriptions.create(
                    model="whisper-1", 
                    file=audio_file,
                    response_format="text"
                )
            
            voice_prompt = transcript
            os.remove(temp_audio_path)
        except Exception as e:
            st.error(f"Transcription failed: {e}")

prompt = st.chat_input("Ask a question about Fordham...")

if voice_prompt:
    prompt = voice_prompt

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
