import pandas as pd
from knowledge_base import mock_data # Import your original data

# --- Prepare DataFrames ---
funds_list = []
fund_secondary_sectors_list = []
fund_related_factors_list = []

for key, fund in mock_data['funds'].items():
    # Main fund data
    funds_list.append({
        'fund_id': fund['id'],
        'internal_key': key, # Keep the original dict key if needed
        'name': fund['name'],
        'amc_id': fund['amc'], # Assuming AMC key is the ID link
        'risk': fund['risk'],
        'primary_sector': fund['primary_sector'], # Assuming sector name is the ID link
        'description': fund['description']
    })
    # Linking table for secondary sectors
    for sector in fund.get('secondary_sectors', []):
        fund_secondary_sectors_list.append({'fund_id': fund['id'], 'sector_id': sector})
    # Linking table for related factors
    for factor in fund.get('related_factors', []):
        fund_related_factors_list.append({'fund_id': fund['id'], 'factor_id': factor})

funds_df = pd.DataFrame(funds_list)
fund_secondary_sectors_df = pd.DataFrame(fund_secondary_sectors_list)
fund_related_factors_df = pd.DataFrame(fund_related_factors_list)

# --- AMCs ---
amcs_list = []
for key, amc in mock_data['amcs'].items():
    amcs_list.append({
        'amc_id': key, # Using the dict key as ID
        'name': amc['name'],
        'established': amc['established'],
        'aum_group': amc['AUM_group']
    })
amcs_df = pd.DataFrame(amcs_list)

# --- Sectors ---
sectors_list = []
for key, sector in mock_data['sectors'].items():
     sectors_list.append({
        'sector_id': key, # Using the dict key as ID
        'name': key, # Name is same as key here
        'description': sector['description'],
        'sensitivity_notes': sector['sensitivity_notes']
    })
sectors_df = pd.DataFrame(sectors_list)

# --- Factors & Links ---
factors_list = []
factor_affected_sectors_list = []
for key, factor in mock_data['factors'].items():
    factors_list.append({
        'factor_id': key, # Using dict key as ID
        'name': key, # Name is same as key here
        'description': factor['description'],
        'impact_direction': factor.get('impact_direction')
    })
    # Linking table for factor -> affected sectors
    for sector in factor.get('typically_affected_sectors', []):
        factor_affected_sectors_list.append({'factor_id': key, 'sector_id': sector})

factors_df = pd.DataFrame(factors_list)
factor_affected_sectors_df = pd.DataFrame(factor_affected_sectors_list)

# --- Save to CSV ---
funds_df.to_csv("funds.csv", index=False)
fund_secondary_sectors_df.to_csv("fund_secondary_sectors.csv", index=False)
fund_related_factors_df.to_csv("fund_related_factors.csv", index=False)
amcs_df.to_csv("amcs.csv", index=False)
sectors_df.to_csv("sectors.csv", index=False)
factors_df.to_csv("factors.csv", index=False)
factor_affected_sectors_df.to_csv("factor_affected_sectors.csv", index=False)

print("CSV files generated successfully!")