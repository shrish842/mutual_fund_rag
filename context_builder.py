import graph_query # Import the module containing query functions

def format_fund_details(fund):
    """Formats details of a single fund nicely."""
    context = f"Fund Name: {fund.get('name')} (ID: {fund.get('id')})\n"
    context += f"Managed by: {fund.get('amc')}\n"
    context += f"Risk Level: {fund.get('risk')}\n"
    context += f"Primary Sector: {fund.get('primary_sector')}\n"
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
    # Limit context length for demo purposes
    display_limit = 5
    limited_list = funds_list[:display_limit]

    for fund in limited_list:
        context += f"- {fund.get('name')} (Risk: {fund.get('risk')}, Primary Sector: {fund.get('primary_sector')}, AMC: {fund.get('amc')})\n"
    if len(funds_list) > display_limit:
        context += f"...and {len(funds_list) - display_limit} more.\n"
    return context

def build_context(intent, entities):
    """Calls graph query functions based on intent and formats results into context string."""
    context = "No specific information found in the knowledge base for this query." # Default message
    results = None # Store results from graph_query

    try:
        if intent == "get_fund_details":
            fund = graph_query.get_fund_details(entities.get("fund_key"))
            if fund: context = format_fund_details(fund)

        elif intent == "find_funds_by_factor":
            factor = entities.get("factor_name")
            results = graph_query.find_funds_related_to_factor(factor)
            context = format_list_of_funds(results, f"potentially affected by '{factor}'")

        elif intent == "find_funds_by_amc":
            amc = entities.get("amc_key")
            results = graph_query.find_funds_by_amc(amc)
            context = format_list_of_funds(results, f"managed by {amc}")

        elif intent == "find_funds_by_sector":
            sector = entities.get("sector_name")
            results = graph_query.find_funds_by_sector(sector)
            context = format_list_of_funds(results, f"investing in the {sector} sector")

        elif intent == "find_funds_by_risk":
             risk = entities.get("risk_level")
             results = graph_query.find_funds_by_risk(risk)
             context = format_list_of_funds(results, f"with '{risk}' risk level")

        elif intent == "get_amc_details":
             amc_key = entities.get("amc_key")
             amc = graph_query.get_amc_details(amc_key)
             if amc: context = f"AMC Details for {amc_key}:\n- Name: {amc.get('name')}\n- Established: {amc.get('established')}\n- AUM Group: {amc.get('AUM_group')}\n"

        elif intent == "get_sector_details":
             sector_name = entities.get("sector_name")
             sector = graph_query.get_sector_details(sector_name)
             if sector: context = f"Sector Details for {sector_name}:\n- Description: {sector.get('description')}\n- Sensitivity Notes: {sector.get('sensitivity_notes')}\n"

        elif intent == "get_factor_details":
             factor_name = entities.get("factor_name")
             factor = graph_query.get_factor_details(factor_name)
             if factor: context = f"Factor Details for {factor_name}:\n- Description: {factor.get('description')}\n- Typical Impact Direction: {factor.get('impact_direction')}\n- Typically Affected Sectors: {', '.join(factor.get('typically_affected_sectors', []))}\n"

        # Add handling for other intents if defined...

    except Exception as e:
        print(f"Error during context building for intent '{intent}' with entities '{entities}': {e}")
        context = f"An error occurred while retrieving information: {e}"

    return context.strip() if context else "Could not retrieve context."