# 🧠 Mutual Fund RAG Assistant (POC)

**A Hackathon Project demonstrating how Retrieval-Augmented Generation (RAG) combined with a Knowledge Graph structure can provide accurate and context-aware answers to complex questions about the mutual fund ecosystem.**

---

## 📝 Table of Contents

- [Problem Statement](#-problem-statement)
- [Our Solution: Graph-Powered RAG](#-our-solution-graph-powered-rag)
- [Key Features](#-key-features)
- [Core RAG Flow](#-core-rag-flow)
- [Technology Stack](#️-technology-stack)
- [Project Structure](#-project-structure)
- [Setup & Installation](#-setup--installation)
- [Usage](#️-usage)
- [Limitations (POC)](#-limitations-poc)
- [Future Work](#-future-work)
- [Team](#-team)

---

## ❓ Problem Statement

The Indian mutual fund landscape is vast and complex. Investors and advisors face challenges in:

1. **Information Overload:** Sifting through thousands of funds, AMCs, prospectuses, and news.
2. **Understanding Relationships:** Grasping how funds, sectors, management companies, and macroeconomic factors (like crude oil prices or interest rates) influence each other.
3. **Getting Reliable Answers:** Standard search engines or generic AI often fail to provide accurate, context-aware answers to nuanced, relationship-based questions (e.g., "Which funds managed by AMC X are most sensitive to interest rate changes?").

---

## 💡 Our Solution: Graph-Powered RAG

This project demonstrates a **Retrieval-Augmented Generation (RAG)** system enhanced by a structured **Knowledge Graph** approach (simulated in this Proof of Concept) to address these challenges.

1. **Knowledge Representation:** We model entities (Funds, AMCs, Sectors, Factors) and their crucial relationships (`ManagedBy`, `InvestsIn`, `AffectedBy`) conceptually as a graph. *(In this POC, this graph is simulated using Python dictionaries for rapid development)*.
2. **RAG Pipeline:**
   - **Retrieve:** When a user asks a question, we first query our knowledge base (the simulated graph) to find relevant entities *and* their connections.
   - **Augment:** The factual, structured information retrieved from the graph is formatted into a context snippet.
   - **Generate:** This context, along with the original query, is fed to a powerful Large Language Model (Google Gemini). The LLM is instructed to generate an answer based *only* on the provided factual context.

**The Result:** Answers are grounded in specific data, are more reliable, and can address complex relational queries that generic models struggle with.

---

## ✨ Key Features (POC)

- **Basic Intent Recognition:** Identifies user intent (e.g., find fund details, find funds by factor) using keyword matching.
- **Simulated Graph Querying:** Retrieves data and relationship information from the hardcoded Python dictionary structure.
- **Relational Context Building:** Can find funds affected by factors directly or indirectly via sector links.
- **LLM Integration:** Uses Google Gemini API for natural language answer generation.
- **Contextual Answer Generation:** Provides answers based on retrieved knowledge, reducing hallucination.
- **Web Interface:** Simple UI built with Streamlit for interaction and demo purposes.

---

## 🔄 Core RAG Flow

```mermaid
graph LR
    A[User Query] --> B{Intent Parser};
    B -- Intent & Entities --> C{Context Builder};
    C -- Query Specs --> D[Graph Query (Simulated)];
    D -- Retrieved Data --> C;
    C -- Formatted Context --> E{LLM Prompt};
    A -- Original Query --> E;
    E -- Augmented Prompt --> F[LLM (Gemini)];
    F -- Grounded Answer --> G[Display to User];
