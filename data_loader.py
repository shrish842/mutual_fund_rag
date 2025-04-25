# data_loader.py
import pandas as pd
import os

# Get the directory where this script is located
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def load_data():
    """Loads all data from CSV files into Pandas DataFrames."""
    try:
        funds_df = pd.read_csv(os.path.join(_SCRIPT_DIR,"funds.csv"))
        fund_secondary_sectors_df = pd.read_csv(os.path.join(_SCRIPT_DIR,"fund_secondary_sectors.csv"))
        fund_related_factors_df = pd.read_csv(os.path.join(_SCRIPT_DIR,"fund_related_factors.csv"))
        amcs_df = pd.read_csv(os.path.join(_SCRIPT_DIR,"amcs.csv"))
        sectors_df = pd.read_csv(os.path.join(_SCRIPT_DIR,"sectors.csv"))
        factors_df = pd.read_csv(os.path.join(_SCRIPT_DIR,"factors.csv"))
        factor_affected_sectors_df = pd.read_csv(os.path.join(_SCRIPT_DIR,"factor_affected_sectors.csv"))

        # Optional: Convert IDs to string if they might be mixed types or for easier merging
        # funds_df['fund_id'] = funds_df['fund_id'].astype(str)
        # amcs_df['amc_id'] = amcs_df['amc_id'].astype(str)
        # ... etc.

        print("Data loaded successfully from CSV files.")

        return {
            "funds": funds_df,
            "fund_secondary_sectors": fund_secondary_sectors_df,
            "fund_related_factors": fund_related_factors_df,
            "amcs": amcs_df,
            "sectors": sectors_df,
            "factors": factors_df,
            "factor_affected_sectors": factor_affected_sectors_df
        }
    except FileNotFoundError as e:
        print(f"Error loading data: {e}. Make sure CSV files exist.")
        # Handle error appropriately - maybe exit or return None
        return None
    except Exception as e:
        print(f"An unexpected error occurred during data loading: {e}")
        return None

# Load data once when the module is imported
loaded_data = load_data()

# Make individual dataframes accessible if needed directly (optional)
if loaded_data:
    funds_df = loaded_data["funds"]
    amcs_df = loaded_data["amcs"]
    sectors_df = loaded_data["sectors"]
    factors_df = loaded_data["factors"]
    fund_secondary_sectors_df = loaded_data["fund_secondary_sectors"]
    fund_related_factors_df = loaded_data["fund_related_factors"]
    factor_affected_sectors_df = loaded_data["factor_affected_sectors"]
else:
    # Define empty DataFrames or handle error if loading failed
    funds_df = pd.DataFrame()
    # ... etc.