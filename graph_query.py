from knowledge_base import mock_data

def get_fund_details(fund_key):
    """Returns details for a specific fund key."""
    return mock_data['funds'].get(fund_key)

def get_amc_details(amc_key):
    """Returns details for a specific AMC key."""
    return mock_data['amcs'].get(amc_key)

def get_sector_details(sector_name):
    """Returns details for a specific sector name."""
    # Sectors are keyed by name in mock_data
    return mock_data['sectors'].get(sector_name)

def get_factor_details(factor_name):
     """Returns details for a specific factor name."""
     # Factors are keyed by name in mock_data
     return mock_data['factors'].get(factor_name)

def find_funds_by_amc(amc_key):
    """Finds all funds managed by a specific AMC key."""
    return [
        details for key, details in mock_data['funds'].items()
        if details.get('amc') == amc_key
    ]

def find_funds_by_sector(sector_name):
    """Finds all funds investing significantly in a specific sector."""
    funds = []
    for key, details in mock_data['funds'].items():
        # Check if the sector name matches primary or is in secondary sectors
        if details.get('primary_sector') == sector_name or \
           sector_name in details.get('secondary_sectors', []):
            funds.append(details)
    return funds

def find_funds_related_to_factor(factor_name):
    """Finds funds directly linked or investing in sectors typically affected by a factor."""
    related_funds_dict = {} # Use dict to avoid duplicates based on fund id

    # 1. Direct link check
    for key, details in mock_data['funds'].items():
        if factor_name in details.get('related_factors', []):
            related_funds_dict[details['id']] = details # Add using unique ID as key

    # 2. Indirect link via sector sensitivity check
    factor_info = get_factor_details(factor_name)
    if factor_info:
        affected_sectors = factor_info.get('typically_affected_sectors', [])
        for sector in affected_sectors:
            # Find funds investing in this affected sector
            funds_in_sector = find_funds_by_sector(sector)
            for fund in funds_in_sector:
                # Add fund to dict if not already present
                related_funds_dict[fund['id']] = fund

    # Return the unique funds as a list
    return list(related_funds_dict.values())

def find_funds_by_risk(risk_level):
    """Finds funds matching a specific risk level (case-insensitive)."""
    return [
        details for key, details in mock_data['funds'].items()
        if details.get('risk', '').lower() == risk_level.lower()
    ]