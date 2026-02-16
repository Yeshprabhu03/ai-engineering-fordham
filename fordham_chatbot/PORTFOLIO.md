# Fordham University AI Assistant: An Engineering Case Study
Click here to view: https://ai-engineering-fordham-chatbot.streamlit.app/
## **Executive Summary**
I engineered a production-ready **Retrieval-Augmented Generation (RAG)** system that serves as an intelligent guide for Fordham University. The goal was to transform ~49,000 unstructured documents into a responsive, verifiable, and cost-efficient AI agent.

What started as a simple chatbot evolved into a lesson in **cloud deployment optimization, vector search engineering, and UI/UX design**.

---

## **Technical Architecture**

### **1. The RAG Pipeline (Retrieval-Augmented Generation)**
Instead of relying on a model's frozen training data, I built a system that "reads" Fordham's data in real-time.
*   **Ingestion**: Scraped and processed **~49,000 documents** (course catalogs, faculty bios, event pages).
*   **Embeddings**: Switched from local HuggingFace models to **OpenAI `text-embedding-3-small`**.
    *   *Why?* Local embedding (e.g., BERT/Sentence-Transformers) was CPU-heavy and slow for 50k docs. OpenAI's text-embedding-3 is faster, cheaper, and has state-of-the-art semantic performance.
*   **Vector Search**: Pre-computed embeddings into a NumPy array (`embeddings.npy`) for **zero-latency** cosine similarity search. No heavy vector database (like Pinecone) was needed for this scale, reducing complexity and cost.

### **2. Token Efficiency & Context Window Management**
LLMs have finite context windows. Sending 50,000 documents is impossible and expensive. I implemented strict **Context Engineering**:
*   **Top-K Retrieval**: The system strictly retrieves only the **top 5** most relevant chunks based on cosine similarity scores. This ensures the model only sees high-signal data.
*   **Sliding Window Memory**: To prevent the "Context Window Overflow" error during long conversations, I implemented a sliding window storage that only retains the **last 4 turns** of conversation. This keeps the prompt lean while maintaining conversational continuity.
*   **Model Selection**: Defaulted to `gpt-4o-mini`. It offers near-GPT-4 intelligence at **95% lower cost** and significantly lower latency, making the app feel "instant".

---

## **Key Engineering Challenges & Solutions**

### **Challenge 1: The "Deployment Hell" (Resource Constraints)**
**The Problem**: My initial deployment on Streamlit Cloud crashed instantly.
*   *Error*: "Memory Limit Exceeded" / "Disk Space Full".
*   *Cause*: I was trying to install `torch` and `sentence-transformers` (1GB+ libraries) to run embeddings locally on the cloud server.

**The Solution: Decoupled Architecture**
I re-architected the app to separate **Build Time** from **Run Time**.
1.  **Offline Processing**: I moved the heavy embedding generation to my local machine.
2.  **Artifact Deployment**: I saved the vectors to a lightweight file (`processed_fordham.pkl`).
3.  **Lean Runtime**: The cloud app now contains *zero* heavy AI libraries. It simply loads the pre-computed arrays and uses API calls.
    *   *Result*: Build time dropped from **15 minutes to 30 seconds**. App size reduced by **90%**.

### **Challenge 2: Git Large File Storage (LFS)**
**The Problem**: GitHub rejected my push because the vector file was >100MB.
**The Solution**: Implemented **Git LFS** to pointer-ize large assets, keeping the repository clean while allowing seamless deployment.

### **Challenge 3: Mobile-Responsive UI & The "Invisible Mic"**
**The Problem**: I wanted a voice input button *inside* the chat bar, like ChatGPT’s mobile app. Standard Streamlit components forced it into a sidebar or disjointed block. CSS positioning (`fixed`, `absolute`) broke on different screen sizes (mobile vs. ultrawide monitors).

**The Solution: The "Centered Overlay" Strategy**
I engineered a custom CSS hack:
1.  Created an **invisible container** (pointer-events: none) that perfectly mirrors the chat input's dimensions (max-width: 800px, centered).
2.  Anchored the microphone button *inside* this invisible container via Flexbox.
3.  *Result*: The microphone now mathematically tracks the input bar on **any device**, from an iPhone SE to a 4K monitor.

---

## **Final Outcome**
*   **Performance**: Sub-second retrieval latency.
*   **UX**: "Oat-inspired" minimalist design with a clean, distraction-free interface.
*   **Reliability**: Zero deployment timeouts; 99.9% uptime.
*   **Features**: Voice-to-Text (Whisper), verifiable citations, and mobile-responsive layout.

This project demonstrates not just how to *call* an API, but how to **engineer a system** around it that is performant, cost-effective, and user-friendly.

---
**Tech Stack**: Python, Streamlit, OpenAI API (GPT-4o-mini, Whisper, Embeddings), Pandas, NumPy, Git LFS, CSS/HTML.
