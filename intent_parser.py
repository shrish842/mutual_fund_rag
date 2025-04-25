# intent_parser.py
# Import DataFrames from the new data loader module
from data_loader import funds_df, amcs_df, sectors_df, factors_df # Import DFs

def parse_intent(query):
    """
    Basic intent/entity recognition based on keywords, now using DataFrames.
    Returns: (intent_type, entities_dictionary)
    """
    query_lower = query.lower()
    entities = {}

    # Check DataFrames are loaded before proceeding
    if funds_df is None or amcs_df is None or sectors_df is None or factors_df is None:
        print("Warning: DataFrames not loaded in intent_parser. Cannot parse intent.")
        return "error", {"message": "Data not loaded"}

    # Priority 1: Check for specific factor names
    # Use the 'name' column from the DataFrame for matching
    if not factors_df.empty:
        for index, factor_row in factors_df.iterrows():
            factor_name = factor_row['name'] # Get name for matching
            factor_id = factor_row['factor_id'] # Get ID to store if matched
            if factor_name.lower() in query_lower:
                entities['factor_id'] = factor_id # Store the ID
                # Check for relationship keywords
                if "affect" in query_lower or "impact" in query_lower or "related" in query_lower or "sensitive" in query_lower:
                     return "find_funds_by_factor", entities
                else:
                     return "get_factor_details", entities

    # Priority 2: Check for specific fund names
    # Use the 'name' column for matching
    if not funds_df.empty:
         for index, fund_row in funds_df.iterrows():
              fund_name = fund_row['name']
              # Store the internal_key used by graph_query.get_fund_details
              fund_internal_key = fund_row['internal_key']
              if fund_name.lower() in query_lower:
                   entities['fund_internal_key'] = fund_internal_key # Store the key needed by graph_query
                   return "get_fund_details", entities

    # Priority 3: Check for specific AMC names or IDs
    # Use 'name' and 'amc_id' columns for matching
    if not amcs_df.empty:
        for index, amc_row in amcs_df.iterrows():
            amc_name = amc_row['name']
            amc_id = amc_row['amc_id']
            # Check if either the name or ID appears in the query
            if amc_name.lower() in query_lower or amc_id.lower() in query_lower:
                entities['amc_id'] = amc_id # Store the ID
                # Check if user asks about funds managed by this AMC
                if "funds" in query_lower or "manage" in query_lower or "portfolio" in query_lower:
                    return "find_funds_by_amc", entities
                else:
                    return "get_amc_details", entities

    # Priority 4: Check for specific Sector names or IDs
    # Use 'name' and 'sector_id' columns for matching
    if not sectors_df.empty:
        for index, sector_row in sectors_df.iterrows():
             sector_name = sector_row['name']
             sector_id = sector_row['sector_id']
             # Check if either the name or ID appears in the query
             if sector_name.lower() in query_lower or sector_id.lower() in query_lower:
                 entities['sector_id'] = sector_id # Store the ID
                 # If query asks for funds investing in this sector
                 if "funds" in query_lower or "invest" in query_lower:
                     return "find_funds_by_sector", entities
                 else:
                     return "get_sector_details", entities

    # Priority 5: Check for risk levels mentioned alongside 'fund'/'funds'
    # This logic doesn't depend on iterating entities, so it remains similar
    risk_keywords = ["risk", "risky", "safe", "level"]
    risk_levels = ["high", "medium", "low"] # Should match values in your funds.csv 'risk' column
    identified_risk = None
    for level in risk_levels:
        if level in query_lower:
            identified_risk = level
            break

    # Check if 'fund' or 'funds' is also mentioned
    if identified_risk and ("fund" in query_lower or "funds" in query_lower):
        # Pass the matched risk level (e.g., 'High', 'Medium') as expected by graph_query
        entities['risk_level'] = identified_risk.capitalize()
        return "find_funds_by_risk", entities

    # Default fallback if no specific pattern is matched
    return "unknown", entities