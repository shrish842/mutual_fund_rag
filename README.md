# 🧠 Mutual Fund RAG Assistant (POC)

**A Hackathon Project demonstrating how Retrieval-Augmented Generation (RAG) combined with a Knowledge Graph structure can provide accurate and context-aware answers to complex questions about the mutual fund ecosystem.**

---

## 📝 Table of Contents

*   [Problem Statement](#problem-statement)
*   [Our Solution: Graph-Powered RAG](#our-solution-graph-powered-rag)
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

## 💡 Our Solution: Graph-Powered RAG

This project demonstrates a **Retrieval-Augmented Generation (RAG)** system enhanced by a structured **Knowledge Graph** approach (simulated in this Proof of Concept) to address these challenges.

1.  **Knowledge Representation:** We model entities (Funds, AMCs, Sectors, Factors) and their crucial relationships (`ManagedBy`, `InvestsIn`, `AffectedBy`) conceptually as a graph. *(In this POC, this graph is simulated using Python dictionaries for rapid development)*.
2.  **RAG Pipeline:**
    *   **Retrieve:** When a user asks a question, we first query our knowledge base (the simulated graph) to find relevant entities *and* their connections.
    *   **Augment:** The factual, structured information retrieved from the graph is formatted into a context snippet.
    *   **Generate:** This context, along with the original query, is fed to a powerful Large Language Model (Google Gemini). The LLM is instructed to generate an answer based *only* on the provided factual context.

**The Result:** Answers are grounded in specific data, are more reliable, and can address complex relational queries that generic models struggle with.

---

## ✨ Key Features (POC)

*   **Basic Intent Recognition:** Identifies user intent (e.g., find fund details, find funds by factor) using keyword matching.
*   **Simulated Graph Querying:** Retrieves data and relationship information from the hardcoded Python dictionary structure.
*   **Relational Context Building:** Can find funds affected by factors directly or indirectly via sector links.
*   **LLM Integration:** Uses Google Gemini API for natural language answer generation.
*   **Contextual Answer Generation:** Provides answers based on retrieved knowledge, reducing hallucination.
*   **Web Interface:** Simple UI built with Streamlit for interaction and demo purposes.

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
Use code with caution.
Markdown
⚙️ Technology Stack
Backend/Core Logic: Python 3.x
Web Framework: Streamlit (for rapid UI development)
LLM API: Google Gemini API (google-generativeai library)
Environment Management: venv
API Key Management: python-dotenv (.env file)
Knowledge Base (POC): Python Dictionaries
📁 Project Structure
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
Use code with caution.
🚀 Setup & Installation
Clone the Repository:
# Replace <your-repo-url> with the actual URL from GitHub
git clone <your-repo-url>
cd mutual-fund-rag
Use code with caution.
Bash
Create and Activate Virtual Environment:
# Create venv
python -m venv venv
# Activate venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
Use code with caution.
Bash
Install Dependencies:
pip install -r requirements.txt
Use code with caution.
Bash
Set Up API Key:
Create a file named .env in the project root directory (mutual_fund_rag/).
Get your API key from Google AI Studio.
Add the following line to the .env file, replacing the placeholder with your actual key:
GOOGLE_API_KEY=YOUR_ACTUAL_GOOGLE_API_KEY_HERE
Use code with caution.
Dotenv
IMPORTANT: Ensure .env is listed in your .gitignore file. Never commit your .env file!
▶️ Usage
Ensure your virtual environment (venv) is activated. (You should see (venv) in your terminal prompt).
Run the Streamlit application:
streamlit run app.py
Use code with caution.
Bash
Open the local URL provided by Streamlit (usually http://localhost:8501) in your web browser.
Enter your questions about the funds, factors, or AMCs defined in knowledge_base.py into the text input box.
Example: Tell me about FundC Infrastructure
Example: Which funds are affected by Crude Oil Price?
Example: What funds does AMC_X manage?
Click "Ask Assistant".
Observe the detected intent/entities, the retrieved context (expand the section!), and the final answer generated by Gemini.
⚠️ Limitations (POC)
Simulated Knowledge: Uses a very small, hardcoded dataset. Not real-time or comprehensive.
Basic Intent Parsing: Relies on simple keyword matching; fails on complex sentence structures.
No True Graph Database: Dictionary lookups are not scalable or efficient for complex graph traversals.
Limited Scope: Only models a few entity and relationship types.
Static: Knowledge base does not update automatically.
🌱 Future Work
Real Data Integration: Connect to live data sources (AMFI, SEBI, news APIs, financial data providers).
Graph Database Implementation: Migrate knowledge base to Neo4j, Neptune, or TigerGraph for scalability and advanced querying.
Advanced NLU: Implement robust Natural Language Understanding using libraries like spaCy or fine-tuned models.
Richer Graph Schema: Add more node types (stocks, fund managers, news articles) and relationships (performance correlation, sentiment links).
Explainability: Enhance context generation to show why entities are related.
Enhanced Features: Portfolio analysis, personalized recommendations, risk simulation, "what-if" scenarios.
👥 Team
[Replace with Your Name/Team Member 1 Name]
[Replace with Team Member 2 Name (if applicable)]
... (Add other team members if any)
