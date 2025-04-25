from knowledge_base import mock_data

def parse_intent(query):
    """
    Very basic intent and entity recognition based on keywords.
    Returns: (intent_type, entities_dictionary)
    """
    query_lower = query.lower()
    entities = {}

    # Priority 1: Check for specific factor names
    for factor_name in mock_data['factors']:
        if factor_name.lower() in query_lower:
            entities['factor_name'] = factor_name
            # If query asks about effect/impact/relation -> find related funds
            if "affect" in query_lower or "impact" in query_lower or "related" in query_lower or "sensitive" in query_lower:
                 return "find_funds_by_factor", entities
            # Otherwise, just provide details about the factor itself
            else:
                 return "get_factor_details", entities

    # Priority 2: Check for specific fund names
    for key, fund_details in mock_data['funds'].items():
        # Check if fund name is mentioned (allows partial matches like "FundC")
        if fund_details['name'].lower() in query_lower:
            entities['fund_key'] = key
            # Simple case: Just asking about the fund
            return "get_fund_details", entities

    # Priority 3: Check for specific AMC names or keys
    for key, amc_details in mock_data['amcs'].items():
        if key.lower() in query_lower or amc_details['name'].lower() in query_lower:
            entities['amc_key'] = key
            # If query asks for funds managed by this AMC
            if "funds" in query_lower or "manage" in query_lower or "portfolio" in query_lower:
                return "find_funds_by_amc", entities
            # Otherwise, just get details about the AMC
            else:
                return "get_amc_details", entities

    # Priority 4: Check for specific Sector names
    for sector_name in mock_data['sectors']:
        if sector_name.lower() in query_lower:
             entities['sector_name'] = sector_name
             # If query asks for funds investing in this sector
             if "funds" in query_lower or "invest" in query_lower:
                 return "find_funds_by_sector", entities
             # Otherwise, just get details about the sector
             else:
                 return "get_sector_details", entities

    # Priority 5: Check for risk levels mentioned alongside 'fund'/'funds'
    risk_keywords = ["risk", "risky", "safe", "level"] # Added 'level'
    risk_levels = ["high", "medium", "low"] # Add more if defined in data
    identified_risk = None
    for level in risk_levels:
        if level in query_lower:
            identified_risk = level
            break # Found a risk level

    # Check if 'fund' or 'funds' is also mentioned
    if identified_risk and ("fund" in query_lower or "funds" in query_lower):
        # Check if a specific risk keyword is nearby (optional refinement)
        # For simplicity, we assume if risk level and 'fund' are present, this is the intent
        entities['risk_level'] = identified_risk.capitalize() # Match case in data ('High', 'Medium')
        return "find_funds_by_risk", entities

    # Default fallback if no specific pattern is matched
    return "unknown", entities