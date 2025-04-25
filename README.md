# 🧠 Mutual Fund RAG Assistant (POC)

**A Hackathon Project demonstrating how Retrieval-Augmented Generation (RAG) combined with a structured Knowledge Base (loaded from CSVs) can provide accurate and context-aware answers to complex questions about the mutual fund ecosystem.**

---

## 📝 Table of Contents

*   [Problem Statement](#problem-statement)
*   [Our Solution: Graph-Powered RAG with CSV Data](#our-solution-graph-powered-rag-with-csv-data)
*   [Key Features](#key-features)
*   [Core RAG Flow](#core-rag-flow)
*   [Technology Stack](#technology-stack)
*   [Project Structure](#project-structure)
*   [Setup & Installation](#setup--installation)
*   [Usage](#usage)
*   [Limitations (POC)](#limitations-poc)
*   [Future Work](#future-work)
*   [Team](#team)

---

## ❓ Problem Statement

The Indian mutual fund landscape is vast and complex. Investors and advisors face challenges in:

1.  **Information Overload:** Sifting through thousands of funds, AMCs, prospectuses, and news.
2.  **Understanding Relationships:** Grasping how funds, sectors, management companies, and macroeconomic factors (like crude oil prices or interest rates) influence each other.
3.  **Getting Reliable Answers:** Standard search engines or generic AI often fail to provide accurate, context-aware answers to nuanced, relationship-based questions (e.g., "Which funds managed by AMC X are most sensitive to interest rate changes?").

---

## 💡 Our Solution: Graph-Powered RAG with CSV Data

This project demonstrates a **Retrieval-Augmented Generation (RAG)** system enhanced by a structured **Knowledge Base** approach to address these challenges. The knowledge (entities and relationships) is loaded from **CSV files** using Pandas.

1.  **Knowledge Representation:** We model entities (Funds, AMCs, Sectors, Factors) and their crucial relationships (`ManagedBy`, `InvestsIn`, `AffectedBy`) conceptually as a graph. *(In this POC, the data representing this graph structure is loaded from `.csv` files into Pandas DataFrames for processing)*.
2.  **RAG Pipeline:**
    *   **Retrieve:** When a user asks a question, we first query our knowledge base (the Pandas DataFrames) to find relevant entities *and* simulate relationship traversal using Pandas operations.
    *   **Augment:** The factual, structured information retrieved is formatted into a context snippet.
    *   **Generate:** This context, along with the original query, is fed to a powerful Large Language Model (Google Gemini). The LLM is instructed to generate an answer based *only* on the provided factual context.

**The Result:** Answers are grounded in specific data loaded from external files, are more reliable, and can address complex relational queries that generic models struggle with.

---

## ✨ Key Features (POC)

*   **Data Loading from CSVs:** Loads knowledge base from structured `.csv` files using Pandas.
*   **Pandas-Based Querying:** Retrieves data and simulates relationship lookups using Pandas DataFrames.
*   **Basic Intent Recognition:** Identifies user intent (e.g., find fund details, find funds by factor) using keyword matching against loaded data.
*   **Relational Context Building:** Can find funds affected by factors directly or indirectly via sector links by joining/filtering DataFrames.
*   **LLM Integration:** Uses Google Gemini API for natural language answer generation.
*   **Contextual Answer Generation:** Provides answers based on retrieved knowledge, reducing hallucination.
*   **(Optional) Basic Explainability:** Can provide simple reasoning for factor-fund relationships.
*   **(Optional) Simple Visualization:** Includes a basic chart (e.g., funds by risk level) for certain queries.
*   **Web Interface:** Simple UI built with Streamlit for interaction and demo purposes.

---


---

## ⚙️ Technology Stack

- **Backend/Core Logic:** Python 3.x  
- **Web Framework:** Streamlit (for rapid UI development)  
- **LLM API:** Google Gemini API (`google-generativeai` library)  
- **Environment Management:** `venv`  
- **API Key Management:** `python-dotenv` (.env file)  
- **Knowledge Base (POC):** Python Dictionaries  

---

## 📁 Project Structure

```
mutual_fund_rag/
├── venv/                     # Virtual environment files (Ignored by Git)
├── .env                      # Stores secret API keys (MUST NOT be committed)
├── .gitignore                # Specifies files/folders for Git to ignore
├── app.py                    # Main Streamlit application script
├── context_builder.py        # Logic to format retrieved data for LLM context
├── graph_query.py            # Functions to query the simulated knowledge graph
├── intent_parser.py          # Basic logic to understand user input
├── knowledge_base.py         # Hardcoded data simulating the graph
├── llm_handler.py            # Handles interaction with the Google Gemini API
└── requirements.txt          # Lists project dependencies
```

---

## 🚀 Setup & Installation

### 1. Clone the Repository

```bash
# Replace <your-repo-url> with the actual URL from GitHub
git clone <your-repo-url>
cd mutual-fund-rag
```

### 2. Create and Activate Virtual Environment

```bash
# Create the environment:
python -m venv venv

# Activate the environment:
# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up API Key

Create a `.env` file in the root project directory:

```dotenv
GOOGLE_API_KEY=YOUR_ACTUAL_GOOGLE_API_KEY_HERE
```

✅ **Make sure `.env` is in `.gitignore`**

---

## ▶️ Usage

1. **Activate the virtual environment:**

```bash
# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate
```

2. **Run the Streamlit app:**

```bash
streamlit run app.py
```

3. **Open in Browser:**  
Visit `http://localhost:8501` (Streamlit will show the URL in the terminal).

4. **Interact with the App:**

Try sample queries like:

- `Tell me about FundC Infrastructure`
- `Which funds are affected by Crude Oil Price?`
- `What funds does AMC_X manage?`

## 🌱 Future Work

- **Graph Database Backend:** Neo4j, TigerGraph, or AWS Neptune.
- **Advanced NLP/NLU:** spaCy, transformers, or custom LLM fine-tuning.
- **Expanded Schema:** Include fund managers, news articles, stocks, and more.
- **Context Explainability:** Visualize reasoning and graph path.
- **Advanced Tools:** Personalized portfolios, what-if analysis, risk models.

---

## 👥 Team

- [Deepali Gupta / Team Member 1]
- [Unnati Gupta / Team Member 2]
- [Udit Mishra / Team Member 3]
- [Shrish Agrawal / Team Member 4]

---

## 📄 License

[Add your license here if applicable]
