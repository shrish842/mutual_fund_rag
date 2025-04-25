mock_data = {
    "funds": {
        "FundA_Growth": {
            "id": "F001",
            "name": "FundA Growth",
            "amc": "AMC_X",
            "risk": "High",
            "primary_sector": "Technology",
            "secondary_sectors": ["Finance"],
            "related_factors": ["Interest Rates", "Chip Shortage"],
            "description": "Aggressively invests in high-growth technology stocks and some finance."
        },
        "FundB_Balanced": {
            "id": "F002",
            "name": "FundB Balanced",
            "amc": "AMC_Y",
            "risk": "Medium",
            "primary_sector": "Diversified",
            "secondary_sectors": ["Finance", "Healthcare", "Consumer Goods"],
            "related_factors": ["Inflation", "GDP Growth"],
            "description": "A balanced fund aiming for steady growth across various sectors."
        },
        "FundC_Infra": {
            "id": "F003",
            "name": "FundC Infrastructure",
            "amc": "AMC_X",
            "risk": "Medium",
            "primary_sector": "Infrastructure",
            "secondary_sectors": ["Energy", "Construction Materials"],
            "related_factors": ["Government Spending", "Crude Oil Price", "Interest Rates"],
            "description": "Focuses on companies involved in infrastructure development and related sectors like energy."
        },
        "FundD_Energy": {
            "id": "F004",
            "name": "FundD Energy Focus",
            "amc": "AMC_Z",
            "risk": "High",
            "primary_sector": "Energy",
            "secondary_sectors": ["Chemicals"],
            "related_factors": ["Crude Oil Price", "Geopolitical Tension", "Renewable Policy"],
            "description": "Concentrated investments in the energy sector, sensitive to oil prices."
        }
    },
    "amcs": {
        "AMC_X": {"id": "A001", "name": "Alpha Management Corp", "established": 2005, "AUM_group": "Large"},
        "AMC_Y": {"id": "A002", "name": "Beta Investments", "established": 2010, "AUM_group": "Medium"},
        "AMC_Z": {"id": "A003", "name": "Zenith Capital", "established": 2015, "AUM_group": "Small"}
    },
    "sectors": {
        "Technology": {"id": "S001", "description": "Companies involved in software, hardware, internet services.", "sensitivity_notes": "Sensitive to interest rates, innovation cycles."},
        "Finance": {"id": "S002", "description": "Banks, insurance companies, financial services.", "sensitivity_notes": "Sensitive to interest rates, regulations."},
        "Healthcare": {"id": "S003", "description": "Pharmaceuticals, hospitals, medical devices.", "sensitivity_notes": "Sensitive to regulations, R&D success."},
        "Infrastructure": {"id": "S004", "description": "Construction, utilities, transportation infrastructure.", "sensitivity_notes": "Sensitive to government spending, interest rates, commodity prices (like oil for transport)."},
        "Energy": {"id": "S005", "description": "Oil & gas exploration, production, refineries, power generation.", "sensitivity_notes": "Highly sensitive to Crude Oil Price, geopolitical events, environmental regulations."},
        "Consumer Goods": {"id": "S006", "description": "Companies making everyday products.", "sensitivity_notes": "Sensitive to inflation, consumer spending."},
        "Construction Materials": {"id": "S007", "description": "Cement, steel for construction.", "sensitivity_notes": "Sensitive to infrastructure spending, housing market."},
        "Chemicals": {"id": "S008", "description": "Industrial and specialty chemicals.", "sensitivity_notes": "Sensitive to Crude Oil Price (feedstock), industrial demand."},
        "Diversified": {"id": "S009", "description": "Invests across many sectors, no single dominant one.", "sensitivity_notes": "Reflects broad market trends."}
    },
    "factors": {
        "Crude Oil Price": {"id": "FAC001", "description": "The global price of crude oil.", "impact_direction": "Varies", "typically_affected_sectors": ["Energy", "Chemicals", "Infrastructure", "Consumer Goods"]}, # Added Consumer Goods link
        "Interest Rates": {"id": "FAC002", "description": "Central bank policy rates.", "impact_direction": "Rising rates often negative for growth stocks/tech, positive for banks.", "typically_affected_sectors": ["Technology", "Finance", "Infrastructure"]},
        "Inflation": {"id": "FAC003", "description": "Rate of increase in prices.", "impact_direction": "Affects consumer spending, input costs.", "typically_affected_sectors": ["Consumer Goods", "Diversified"]},
        "GDP Growth": {"id": "FAC004", "description": "Overall economic growth.", "impact_direction": "Positive for most sectors.", "typically_affected_sectors": ["Diversified", "Finance"]},
        "Chip Shortage": {"id": "FAC005", "description": "Supply constraint for semiconductors.", "impact_direction": "Negative for users, positive for producers.", "typically_affected_sectors": ["Technology", "Automotive"]}, # Automotive not explicitly in funds here
        "Government Spending": {"id": "FAC006", "description": "Public expenditure, especially on infrastructure.", "impact_direction": "Positive for related sectors.", "typically_affected_sectors": ["Infrastructure", "Construction Materials"]},
        "Geopolitical Tension": {"id": "FAC007", "description": "International conflicts or instability.", "impact_direction": "Often drives oil prices, uncertainty.", "typically_affected_sectors": ["Energy"]},
        "Renewable Policy": {"id": "FAC008", "description": "Government policies favouring renewable energy.", "impact_direction": "Positive for renewables, potentially negative for fossil fuels.", "typically_affected_sectors": ["Energy"]}
    }
}

# Helper function (optional but potentially useful)
def find_fund_key_by_name(fund_name):
    """Finds the internal key for a fund given its name (case-insensitive)."""
    for key, fund_details in mock_data['funds'].items():
        if fund_name.lower() in fund_details['name'].lower():
            return key
    return None