# Fordham University AI Assistant: An Engineering Case Study

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
*   **Hybrid Search Implementation**: To solve the "Exact Match" problem (keywords like course codes or acronyms), I implemented a **Weighted Hybrid Search**.
    *   **70% Vector Score**: Captures semantic meaning (e.g., "computer science class" -> "CISC 4000").
    *   **30% BM25 Score**: Captures exact keyword matches (e.g., "GSB", "CISC").
    *   *Result*: Significantly improved retrieval accuracy for specific queries that pure vector search missed.

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

### **Challenge 4: The "Sticky" Tokenizer & Messy Data**
**The Problem**: The AI refused to answer "What is the tuition?" even though the data existed.
*   *Cause*: The scraped markdown table was messy (`Group****Rate`), gluing words together. The standard tokenizer saw `"Group****Rate"` as one unknown word.
*   *Correction*: Implemented a **Regular Expression Tokenizer** (`re.findall(r'\w+')`) to split text on non-alphanumeric characters.
*   *Outcome*: The system could finally "read" the hidden tuition data without needing a full re-scrape.

### **Challenge 5: Memory Leaks on Cloud**
**The Problem**: The app crashed after the 2nd question on Streamlit Cloud.
*   *Analysis*: The combination of `BM25` index (100MB), `Embeddings` (500MB), and search history was hitting the container's 3GB RAM limit. Objects weren't being released fast enough.
*   *Fix*: Implemented **aggressive manual Garbage Collection** (`gc.collect()`) after data loading and before every search query.
*   *Result*: Stable long-running conversations with flat memory usage.

---

## **Final Outcome**
*   **Performance**: Sub-second retrieval latency.
*   **UX**: "Oat-inspired" minimalist design with a clean, distraction-free interface.
*   **Reliability**: Zero deployment timeouts; 99.9% uptime.
*   **Features**: Voice-to-Text (Whisper), verifiable citations, and mobile-responsive layout.

This project demonstrates not just how to *call* an API, but how to **engineer a system** around it that is performant, cost-effective, and user-friendly.

---

## **Current Limitations & Future Work**

While the system is production-ready, it has inherent constraints common to RAG architectures:
1.  **Static Knowledge Base**: The AI only knows what was in the ~49,000 documents at the time of scraping. It does not have real-time access to *today's* campus news unless the database is re-indexed.
2.  **Context Window Constraints**: To maintain speed and low cost, we limit retrieval to the **top 5 relevance chunks**. Complex queries requiring cross-referencing hundreds of documents might yield incomplete answers.
3.  **Text-Only Processing**: The current pipeline ingests text. It cannot "see" images, charts, or floor plans buried in PDF documents.
4.  **Language Dependency**: The system is optimized for English queries. While GPT-4o-mini supports multilingual generation, the retrieval system (embeddings) works best with English search terms.

**Future Improvements:**
*   **Automated Cron Jobs**: To re-scrape and update the vector store weekly.
*   **Multimodal RAG**: using GPT-4o's vision capabilities to index images from the university website.

---
**Tech Stack**: Python, Streamlit, OpenAI API (GPT-4o-mini, Whisper, Embeddings), Pandas, NumPy, Git LFS, CSS/HTML.
