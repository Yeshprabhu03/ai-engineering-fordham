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
        background-color: #fcfcfc; /* Oat-like clean white */
        font-family: 'Lato', sans-serif;
        color: #1a1a1a;
    }}
    
    /* Center the main block */
    .main .block-container {{
        max_width: 800px;
        padding-top: 4rem; /* Increased to prevent logo clipping on mobile */
        padding-bottom: 6rem; /* Space for chat input */
    }}

    /* Mobile-Optimized Facts Container */
    .facts-container {{
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        gap: 10px;
        margin-bottom: 20px;
        flex-wrap: nowrap; /* Force horizontal on mobile */
    }}
    .fact-card {{
        background: #fafafa;
        border: 1px solid #eee;
        border-radius: 8px;
        padding: 10px 5px;
        text-align: center;
        flex: 1; /* Equal width */
        min-width: 0; /* Allow shrinking */
    }}
    .fact-icon {{
        font-size: 1.5rem;
        margin-bottom: 5px;
    }}
    .fact-title {{
        font-weight: 700;
        font-size: 0.85rem;
        margin: 0;
        color: #333;
        white-space: nowrap;
    }}
    .fact-sub {{
        font-size: 0.7rem;
        color: #666;
        margin: 0;
    }}

    /* Mobile adjustments for mic (Covered by main media query now) */
    /* @media (max-width: 640px) {{ ... }} */
    
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
    /* Floating Microphone Positioning */
    div.element-container:has(iframe[title="audio_recorder_streamlit.audio_recorder"]) {{
        position: fixed;
        bottom: 30px;
        z-index: 999999;
        width: auto !important;
        height: 0px !important;
        margin: 0px !important;
        overflow: visible !important;
    }}
    
    /* Desktop: Anchor to the centered 800px container */
    @media (min-width: 850px) {{
        div.element-container:has(iframe[title="audio_recorder_streamlit.audio_recorder"]) {{
            left: calc(50% + 400px - 90px); /* Center + Half Width - Offset into bar */
            right: auto !important;
        }}
    }}
    
    /* Mobile: Anchor to the right edge */
    @media (max-width: 849px) {{
        div.element-container:has(iframe[title="audio_recorder_streamlit.audio_recorder"]) {{
            right: 55px !important;
            left: auto !important;
        }}
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
# Centered Logo and Title
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if os.path.exists(logo_path):
        # Use fixed width instead of column width to keep it small
        # Centering trigger: we use a nested column or just markdown 
        # Easier: Just put it in a narrower center column or use st.image with width
        # Let's try making the columns narrower to force centering
        pass
    
# Actually, let's just use a single centered image approach with specific width
if os.path.exists(logo_path):
    col1, col2, col3 = st.columns([3, 1, 3])
    with col2:
        st.image(logo_path, width=80)

st.markdown("<h1 style='text-align: center; color: #860038;'>Fordham University AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 1.1em; color: #555;'>Ask anything about programs, faculty, or campus life.</p>", unsafe_allow_html=True)

# 3 Key Facts / Features (CSS Flexbox for Mobile Stability)
st.markdown("""
<div class="facts-container">
    <div class="fact-card">
        <div class="fact-icon">📚</div>
        <p class="fact-title">~49k Docs</p>
        <p class="fact-sub">Official Data</p>
    </div>
    <div class="fact-card">
        <div class="fact-icon">🔗</div>
        <p class="fact-title">Verifiable</p>
        <p class="fact-sub">Citations</p>
    </div>
    <div class="fact-card">
        <div class="fact-icon">🎙️</div>
        <p class="fact-title">Voice</p>
        <p class="fact-sub">Input</p>
    </div>
</div>
""", unsafe_allow_html=True)

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
