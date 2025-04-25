# context_builder.py
import graph_query
# Import necessary DFs for explanation logic
from data_loader import sectors_df # You might need others depending on explanation detail

# --- Formatting Helper Functions (Keep As Is) ---
def format_fund_details(fund):
    """Formats details of a single fund nicely."""
    if not fund: return "Fund details not found."
    context = f"Fund Name: {fund.get('name')} (ID: {fund.get('fund_id')})\n" # Use fund_id
    context += f"Managed by: {fund.get('amc_id')}\n" # Use amc_id
    context += f"Risk Level: {fund.get('risk')}\n"
    context += f"Primary Sector: {fund.get('primary_sector')}\n"
    # Ensure secondary_sectors and related_factors are retrieved if needed by graph_query.get_fund_details
    if fund.get('secondary_sectors'):
         context += f"Other Sectors: {', '.join(fund.get('secondary_sectors'))}\n"
    if fund.get('related_factors'):
        context += f"Directly Related Factors: {', '.join(fund.get('related_factors'))}\n"
    context += f"Description: {fund.get('description')}\n"
    return context

def format_list_of_funds(funds_list, query_context=""):
    """Formats a list of funds concisely."""
    if not funds_list:
        return "No funds found matching the criteria.\n"

    context = f"Found {len(funds_list)} fund(s) {query_context}:\n"
    display_limit = 5
    limited_list = funds_list[:display_limit]

    for fund in limited_list:
        context += f"- {fund.get('name')} (Risk: {fund.get('risk')}, Primary Sector: {fund.get('primary_sector')}, AMC: {fund.get('amc_id')})\n" # Use amc_id
    if len(funds_list) > display_limit:
        context += f"...and {len(funds_list) - display_limit} more.\n"
    return context

# --- Main build_context Function ---
def build_context(intent, entities):
    """
    Calls graph query functions based on intent, formats results,
    and potentially generates an explanation.
    ALWAYS returns a tuple: (context_string, explanation_string_or_None)
    """
    context = "No specific information found in the knowledge base for this query." # Default context
    explanation = None # Initialize explanation string - MUST always be returned
    results = None # Store raw results if needed

    try:
        # --- Logic for each intent ---
        if intent == "get_fund_details":
            fund = graph_query.get_fund_details(entities.get("fund_internal_key"))
            if fund:
                context = format_fund_details(fund)
            # No explanation generated for this intent typically
            explanation = None

        elif intent == "find_funds_by_factor":
            factor_id = entities.get("factor_id")
            results = graph_query.find_funds_related_to_factor(factor_id)
            context = format_list_of_funds(results, f"potentially affected by '{factor_id}'")

            # --- Add Explanation Logic ---
            if results and factor_id: # Check if results were found
                try:
                    factor_info = graph_query.get_factor_details(factor_id)
                    affected_sector_ids = factor_info.get('typically_affected_sectors', []) if factor_info else []

                    affected_sector_names = []
                    if not sectors_df.empty and affected_sector_ids:
                         affected_sector_names = sectors_df[sectors_df['sector_id'].isin(affected_sector_ids)]['name'].tolist()

                    example_fund = results[0] # Use first fund as example
                    fund_name = example_fund.get('name')
                    fund_primary_sector = example_fund.get('primary_sector')

                    # Construct explanation string
                    explanation = f"Reasoning: The factor '{factor_id}' often affects sectors like {', '.join(affected_sector_names) or 'specific sectors'}. "
                    explanation += f"'{fund_name}' is potentially affected because it invests in '{fund_primary_sector}'"
                    # Add more detail if needed, e.g., about secondary sectors
                    explanation += "."
                except Exception as e:
                    print(f"Error generating explanation: {e}")
                    explanation = "[Could not generate explanation details]"
            else:
                 explanation = None # Ensure explanation is None if no results found

        elif intent == "find_funds_by_amc":
            amc = entities.get("amc_id")
            results = graph_query.find_funds_by_amc(amc)
            context = format_list_of_funds(results, f"managed by {amc}")
            explanation = None # No specific explanation logic here yet

        elif intent == "find_funds_by_sector":
            sector = entities.get("sector_id")
            results = graph_query.find_funds_by_sector(sector)
            context = format_list_of_funds(results, f"investing in the {sector} sector")
            explanation = None # No specific explanation logic here yet

        elif intent == "find_funds_by_risk":
             risk = entities.get("risk_level")
             results = graph_query.find_funds_by_risk(risk)
             context = format_list_of_funds(results, f"with '{risk}' risk level")
             explanation = None # No specific explanation logic here yet

        elif intent == "get_amc_details":
             amc_key = entities.get("amc_id")
             amc = graph_query.get_amc_details(amc_key)
             if amc: context = f"AMC Details for {amc_key}:\n- Name: {amc.get('name')}\n- Established: {amc.get('established')}\n- AUM Group: {amc.get('AUM_group')}\n"
             explanation = None # No specific explanation logic here yet

        elif intent == "get_sector_details":
             sector_name = entities.get("sector_id")
             sector = graph_query.get_sector_details(sector_name)
             if sector: context = f"Sector Details for {sector_name}:\n- Description: {sector.get('description')}\n- Sensitivity Notes: {sector.get('sensitivity_notes')}\n"
             explanation = None # No specific explanation logic here yet

        elif intent == "get_factor_details":
             factor_name = entities.get("factor_id")
             factor = graph_query.get_factor_details(factor_name)
             if factor:
                 affected_sectors_str = ', '.join(factor.get('typically_affected_sectors', [])) or 'N/A'
                 context = f"Factor Details for {factor_name}:\n- Description: {factor.get('description')}\n- Typical Impact Direction: {factor.get('impact_direction')}\n- Typically Affected Sectors: {affected_sectors_str}\n"
             explanation = None # No specific explanation logic here yet

        # Handle unknown or error intents passed from parser
        elif intent == "unknown" or intent == "error":
             context = "Could not process the query due to unknown intent or data issues."
             explanation = None

        else:
             # Fallback for any other unexpected intent
             context = f"Internal Error: Unhandled intent '{intent}'."
             explanation = None

    except Exception as e:
        print(f"Error during context building for intent '{intent}' with entities '{entities}': {e}")
        context = f"An error occurred while retrieving information: {e}"
        explanation = None # Ensure explanation is None on error

    # *** Final Return - ALWAYS return a tuple of 2 items ***
    final_context = context.strip() if isinstance(context, str) else "Error: Invalid context generated."
    final_explanation = explanation.strip() if isinstance(explanation, str) else None

    return (final_context, final_explanation) # Return as a tuple