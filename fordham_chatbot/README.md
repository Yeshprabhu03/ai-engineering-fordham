# Fordham University AI Assistant (RamBot)

This directory contains the production-ready Retrieval-Augmented Generation (RAG) system serving as an intelligent guide for Fordham University.

## 🚀 Live Demo

**[Click here to view and interact with the deployed Streamlit application!](https://your-streamlit-app-url-here.streamlit.app/)**

*(Note: Replace the placeholder URL above with your actual deployed Streamlit link)*

---

## Technical Overview

*   **Ingestion & Vectors:** Scraped ~49,000 documents from Fordham's website. Embedded using OpenAI's `text-embedding-3-small`.
*   **Search Engine:** Implemented a zero-latency **Hybrid Search** combining dense vector similarity (Cosine) with keyword search (BM25) to solve exact-match problems for course codes.
*   **UI/UX:** Features a custom CSS "Centered Overlay" microphone for voice-to-text input (powered by Whisper), and sliding window memory to prevent context overflow.
*   **Decoupled Architecture:** Heavy ML processes (like chunking and embedding) were performed offline. The production cloud app loads lightweight pre-computed NumPy arrays (`embeddings.npy`), keeping the runtime lean and avoiding memory crashes.

For an in-depth dive into the technical challenges and engineering solutions (such as Context Window Optimization, Git LFS integration, and managing Cloud resource limits), please see the main **[PORTFOLIO.md](PORTFOLIO.md)**.
