# graph_query.py
# Import the loaded dataframes from data_loader
from data_loader import (
    funds_df, amcs_df, sectors_df, factors_df,
    fund_secondary_sectors_df, fund_related_factors_df,
    factor_affected_sectors_df, loaded_data # Also import loaded_data dict if needed
)
import pandas as pd

# Helper function to convert DataFrame rows to dictionaries (for compatibility)
def df_to_dict_list(df):
    return df.to_dict('records')

# --- Rewritten Query Functions ---

def get_fund_details(fund_internal_key):
    """Returns details for a specific fund given its original internal key."""
    if funds_df.empty: return None
    fund_series = funds_df[funds_df['internal_key'] == fund_internal_key]
    if not fund_series.empty:
        fund_dict = fund_series.iloc[0].to_dict()
        # Add back related lists (optional, could be done in context_builder)
        fund_id = fund_dict['fund_id']
        sec_sectors = fund_secondary_sectors_df[fund_secondary_sectors_df['fund_id'] == fund_id]['sector_id'].tolist()
        rel_factors = fund_related_factors_df[fund_related_factors_df['fund_id'] == fund_id]['factor_id'].tolist()
        fund_dict['secondary_sectors'] = sec_sectors
        fund_dict['related_factors'] = rel_factors
        return fund_dict
    return None

def get_amc_details(amc_id):
    """Returns details for a specific AMC ID."""
    if amcs_df.empty: return None
    amc_series = amcs_df[amcs_df['amc_id'] == amc_id]
    return amc_series.iloc[0].to_dict() if not amc_series.empty else None

def get_sector_details(sector_id):
    """Returns details for a specific Sector ID."""
    if sectors_df.empty: return None
    sector_series = sectors_df[sectors_df['sector_id'] == sector_id]
    return sector_series.iloc[0].to_dict() if not sector_series.empty else None

def get_factor_details(factor_id):
     """Returns details for a specific Factor ID."""
     if factors_df.empty: return None
     factor_series = factors_df[factors_df['factor_id'] == factor_id]
     if not factor_series.empty:
         factor_dict = factor_series.iloc[0].to_dict()
         # Add back affected sectors
         affected_sectors = factor_affected_sectors_df[factor_affected_sectors_df['factor_id'] == factor_id]['sector_id'].tolist()
         factor_dict['typically_affected_sectors'] = affected_sectors
         return factor_dict
     return None

def find_funds_by_amc(amc_id):
    """Finds all funds managed by a specific AMC ID."""
    if funds_df.empty: return []
    result_df = funds_df[funds_df['amc_id'] == amc_id]
    return df_to_dict_list(result_df)

def find_funds_by_sector(sector_id):
    """Finds all funds investing significantly in a specific sector ID."""
    if funds_df.empty or fund_secondary_sectors_df.empty: return []
    # Funds where it's primary
    primary_funds_df = funds_df[funds_df['primary_sector'] == sector_id]
    # Fund IDs where it's secondary
    secondary_fund_ids = fund_secondary_sectors_df[fund_secondary_sectors_df['sector_id'] == sector_id]['fund_id'].unique()
    secondary_funds_df = funds_df[funds_df['fund_id'].isin(secondary_fund_ids)]
    # Combine and remove duplicates
    combined_df = pd.concat([primary_funds_df, secondary_funds_df]).drop_duplicates(subset=['fund_id'])
    return df_to_dict_list(combined_df)

def find_funds_related_to_factor(factor_id):
    """Finds funds related to a factor (directly or via sectors)."""
    if not loaded_data: return [] # Check if data loading failed

    # Use the pre-loaded DataFrames directly
    _funds = loaded_data["funds"]
    _fund_related = loaded_data["fund_related_factors"]
    _factor_affected = loaded_data["factor_affected_sectors"]
    _fund_secondary = loaded_data["fund_secondary_sectors"]

    if _funds.empty: return []

    related_fund_ids = set()

    # 1. Direct link check
    direct_link_ids = _fund_related[_fund_related['factor_id'] == factor_id]['fund_id'].unique()
    related_fund_ids.update(direct_link_ids)

    # 2. Indirect link via sector sensitivity check
    affected_sectors_ids = _factor_affected[_factor_affected['factor_id'] == factor_id]['sector_id'].unique()

    if len(affected_sectors_ids) > 0:
        # Find funds where primary sector is affected
        primary_sector_funds = _funds[_funds['primary_sector'].isin(affected_sectors_ids)]['fund_id'].unique()
        related_fund_ids.update(primary_sector_funds)

        # Find funds where a secondary sector is affected
        secondary_link_fund_ids = _fund_secondary[_fund_secondary['sector_id'].isin(affected_sectors_ids)]['fund_id'].unique()
        related_fund_ids.update(secondary_link_fund_ids)

    # Retrieve full details for the unique fund IDs
    if not related_fund_ids:
        return []
    final_funds_df = _funds[_funds['fund_id'].isin(list(related_fund_ids))]
    return df_to_dict_list(final_funds_df)


def find_funds_by_risk(risk_level):
    """Finds funds matching a specific risk level (case-insensitive)."""
    if funds_df.empty: return []
    # Ensure comparison is case-insensitive
    result_df = funds_df[funds_df['risk'].str.lower() == risk_level.lower()]
    return df_to_dict_list(result_df)