import streamlit as st
from intent_parser import parse_intent
from context_builder import build_context
from llm_handler import get_llm_response
from knowledge_base import mock_data # To show some available entities

# Configure Streamlit page settings
st.set_page_config(
    page_title="Mutual Fund RAG POC",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Page Header ---
st.title("🧠 Mutual Fund RAG Assistant (POC)")
st.caption("Ask questions about a limited knowledge base of funds, AMCs, sectors, and factors.")
st.markdown("""
*Example Questions:*
*   `Tell me about FundC Infrastructure`
*   `Which funds are managed by AMC_X?`
*   `Show funds investing in the Energy sector`
*   `Which funds are affected by Crude Oil Price?`
*   `What is the risk level of FundA Growth?`
*   `Find high risk funds`
*   `Tell me about Interest Rates`
""")

# --- Optional: Display Knowledge Base Info ---
with st.expander("Explore Entities in Knowledge Base"):
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("Funds")
        st.json({k: v['name'] for k, v in mock_data['funds'].items()}, expanded=False)
    with col2:
        st.subheader("Factors")
        st.json({k: v['description'] for k, v in mock_data['factors'].items()}, expanded=False)
        st.subheader("AMCs")
        st.json({k: v['name'] for k, v in mock_data['amcs'].items()}, expanded=False)
    with col3:
        st.subheader("Sectors")
        st.json(list(mock_data['sectors'].keys()), expanded=False)


# --- Main Interaction Area ---
st.divider() # Visual separator
user_query = st.text_input("Enter your question here:", key="query_input")

if st.button("Ask Assistant", key="ask_button"):
    if user_query:
        st.markdown("---") # Separator before showing results

        # 1. Parse Intent and Entities
        intent, entities = parse_intent(user_query)

        # Display detected intent/entities for debugging/demo
        st.write(f"**Detected Intent:** `{intent}`")
        if entities:
             st.write(f"**Detected Entities:** `{entities}`")
        st.markdown("---") # Separator

        if intent == "unknown":
            st.warning("Sorry, I couldn't fully understand your query based on the available patterns or known entities. Please try rephrasing using terms from the knowledge base explorer above.")
        else:
            # 2. Retrieve Context (Simulated Graph Query)
            st.subheader("Step 1: Retrieving Context from Knowledge Base")
            with st.spinner("Querying simulated graph..."):
                 context = build_context(intent, entities)

            # --- CRUCIAL FOR DEMO: Show the retrieved context ---
            with st.expander("Show Retrieved Context (Passed to LLM)", expanded=False):
                st.text(context if context else "No context was retrieved.")
            # ---

            if not context or "No specific information found" in context or "Could not retrieve context" in context:
                st.warning(f"Could not find relevant information in the knowledge base for: '{user_query}'. Context retrieved: '{context}'")
            else:
                # 3. Augment and Generate Response with LLM
                st.subheader("Step 2: Generating Answer using LLM with Context")
                with st.spinner("Asking the LLM..."):
                    answer = get_llm_response(context, user_query)

                # Display the final answer
                st.success("**Assistant's Answer:**")
                st.markdown(answer) # Use markdown for potentially better formatting

    else:
        st.warning("Please enter a question before clicking 'Ask Assistant'.")