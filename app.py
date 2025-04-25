# app.py
import streamlit as st
import pandas as pd # Ensure pandas is imported

# Import functions/modules - Use the new data_loader
from intent_parser import parse_intent
from context_builder import build_context
from llm_handler import get_llm_response
# Import the DataFrames loaded by data_loader AND the loaded_data dictionary
from data_loader import funds_df, amcs_df, sectors_df, factors_df, loaded_data
# Also import graph_query if needed for re-querying for viz
import graph_query


# Configure Streamlit page settings
st.set_page_config(
    page_title="Mutual Fund RAG POC",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Page Header ---
st.title("🧠 Mutual Fund RAG Assistant (POC)")
st.caption("Ask questions about a knowledge base loaded from CSV files.") # Updated caption
st.markdown("""
*Example Questions:*
*   `Tell me about FundC Infrastructure`
*   `Which funds are managed by AMC_X?`
*   `Show funds investing in the Energy sector`
*   `Which funds are affected by Crude Oil Price?`
*   `Find high risk funds`
*   `Tell me about Interest Rates`
""")

# --- Optional: Display Knowledge Base Info ---
st.subheader("Explore Entities Loaded from Data Files") # Updated title
with st.expander("Click to see sample Funds, Factors, AMCs, Sectors"):
    # Check if data loaded correctly before trying to display
    if not loaded_data:
         st.warning("Data could not be loaded from CSV files. Please check logs and file paths.")
    else:
        col1, col2, col3 = st.columns(3)
        # Display data using the loaded DataFrames
        with col1:
            st.caption("**Funds (Internal Key: Name)**")
            if not funds_df.empty:
                # Create dict {internal_key: name} for display
                display_dict = funds_df[['internal_key', 'name']].set_index('internal_key')['name'].to_dict()
                st.json(display_dict, expanded=False)
            else: st.write("Fund data not loaded.")

            # --- AMCs Moved Here (Correct Location) ---
            st.caption("**AMCs (ID: Name)**")
            if not amcs_df.empty:
                 # Create dict {amc_id: name}
                display_dict = amcs_df[['amc_id', 'name']].set_index('amc_id')['name'].to_dict()
                st.json(display_dict, expanded=False)
            else: st.write("AMC data not loaded.")
            # --- End AMCs ---

        with col2:
            st.caption("**Factors (ID: Name)**")
            if not factors_df.empty:
                 # Create dict {factor_id: name}
                display_dict = factors_df[['factor_id', 'name']].set_index('factor_id')['name'].to_dict()
                st.json(display_dict, expanded=False)
            else: st.write("Factor data not loaded.")

            st.caption("**Sectors (ID: Name)**") # Changed to show ID:Name for consistency
            if not sectors_df.empty:
                 # Create dict {sector_id: name}
                display_dict = sectors_df[['sector_id', 'name']].set_index('sector_id')['name'].to_dict()
                st.json(display_dict, expanded=False)
            else: st.write("Sector data not loaded.")

        with col3:
             # Display row counts as a basic check
             st.subheader("Data Counts")
             st.write(f"- Funds: {len(funds_df)}")
             st.write(f"- AMCs: {len(amcs_df)}")
             st.write(f"- Sectors: {len(sectors_df)}")
             st.write(f"- Factors: {len(factors_df)}")
             # Optionally add counts for linking tables from data_loader.py if needed


# --- Main Interaction Area ---
st.divider() # Visual separator
# Ensure this line is correctly indented at the base level
user_query = st.text_input("Enter your question here:", key="query_input", placeholder="e.g., Which funds are affected by Crude Oil Price?")

# Ensure this 'if' block starts at the base indentation level
if st.button("Ask Assistant", key="ask_button"):
    if user_query:
        # Check if data loaded correctly before proceeding
        # Use the loaded_data dictionary check from data_loader.py
        if not loaded_data:
            st.error("Application Error: Knowledge base data failed to load. Cannot process query.")
        else:
            st.markdown("---") # Separator before showing results

            # 1. Parse Intent and Entities
            intent, entities = parse_intent(user_query)

            # Check for potential error during parsing (e.g., if data wasn't loaded)
            if intent == "error":
                 st.error(f"Application Error: {entities.get('message', 'Could not parse intent due to data issues.')}")
            else:
                # Display detected intent/entities for debugging/demo
                st.write(f"**Detected Intent:** `{intent}`")
                if entities:
                     st.write(f"**Detected Entities:** `{entities}`")
                st.markdown("---") # Separator

                if intent == "unknown":
                    st.warning("Sorry, I couldn't fully understand your query based on the available patterns or known entities. Please try rephrasing using terms from the knowledge base explorer above.")
                else:
                    # 2. Retrieve Context & Explanation (potentially)
                    st.subheader("Step 1: Retrieving Context from Knowledge Base")
                    explanation = None # Initialize explanation
                    results_list_of_dicts = None # Initialize if needed for viz

                    with st.spinner("Querying data source..."):
                        # Call build_context - assuming it returns (context, explanation_or_None)
                        context, explanation = build_context(intent, entities)

                        # Re-run query if needed for visualization (Example: find_funds_by_amc)
                        if intent == "find_funds_by_amc":
                            results_list_of_dicts = graph_query.find_funds_by_amc(entities.get("amc_id"))

                    # Show Retrieved Context
                    with st.expander("Show Retrieved Context (Passed to LLM)", expanded=False):
                        st.text(context if context else "No context was retrieved.")

                    # Display Explanation (if implemented in Priority 2)
                    if explanation:
                        st.info(f"ℹ️ **Explanation:** {explanation}")

                    if not context or "No specific information found" in context or "Could not retrieve context" in context:
                        st.warning(f"Could not find relevant information in the knowledge base for: '{user_query}'. Context retrieved: '{context}'")
                    else:
                        # 3. Augment and Generate Response with LLM
                        st.subheader("Step 2: Generating Answer using LLM with Context")
                        with st.spinner("Asking the LLM..."):
                            answer = get_llm_response(context, user_query) # LLM still only gets context string

                        # Display the final answer
                        st.success("**Assistant's Answer:**")
                        st.markdown(answer)

                        # Display Visualization (if implemented in Priority 3)
                        if intent == "find_funds_by_amc" and results_list_of_dicts is not None:
                            st.divider()
                            st.subheader("Analysis: Funds by Risk Level")
                            if len(results_list_of_dicts) > 0:
                                # Convert list of dicts back to DataFrame for easy plotting
                                viz_df = pd.DataFrame(results_list_of_dicts)
                                risk_counts = viz_df['risk'].value_counts()
                                st.bar_chart(risk_counts)
                            else:
                                st.write("No funds found for this AMC to visualize.")
    else:
        st.warning("Please enter a question before clicking 'Ask Assistant'.")