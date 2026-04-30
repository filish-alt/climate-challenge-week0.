import pandas as pd
import numpy as np
import os

def generate_mock_datasets():
    print("Generating mock datasets...")
    raw_path = '../data/ethiopia.csv'
    
    if not os.path.exists(raw_path):
        print(f"Error: {raw_path} not found.")
        return

    # Load base dataset
    df = pd.read_csv(raw_path, skiprows=9)
    
    # Process base dataset
    df['Date'] = pd.to_datetime(
        df['YEAR'].astype(str) + '-' + df['MO'].astype(str) + '-' + df['DY'].astype(str),
        format='%Y-%m-%d'
    )
    df.set_index('Date', inplace=True)
    
    numeric_cols = ['T2M', 'T2M_MAX', 'T2M_MIN', 'PRECTOTCORR', 'RH2M', 'WS2M', 'WS2M_MAX']
    df[numeric_cols] = df[numeric_cols].replace(-999, np.nan)
    df.drop_duplicates(inplace=True)
    
    threshold = int(0.7 * len(numeric_cols))
    df.dropna(subset=numeric_cols, thresh=threshold, inplace=True)
    df[numeric_cols] = df[numeric_cols].ffill()
    
    # Base configuration for 5 countries (Offsets applied to Temperature, Precipitation, etc.)
    # Ethiopia is the baseline
    countries_config = {
        'Ethiopia': {'T_offset': 0.0, 'P_multiplier': 1.0},
        'Kenya': {'T_offset': 2.5, 'P_multiplier': 1.2},        # Hotter, slightly more rain
        'Somalia': {'T_offset': 5.0, 'P_multiplier': 0.4},      # Much hotter, much drier
        'Sudan': {'T_offset': 7.0, 'P_multiplier': 0.2},        # Hottest, driest
        'Djibouti': {'T_offset': 6.5, 'P_multiplier': 0.3}      # Very hot, very dry
    }
    
    os.makedirs('../data', exist_ok=True)
    
    for country, config in countries_config.items():
        print(f"Generating data for {country}...")
        df_country = df.copy()
        
        # Apply offsets
        df_country['T2M'] = df_country['T2M'] + config['T_offset']
        df_country['T2M_MAX'] = df_country['T2M_MAX'] + config['T_offset']
        df_country['T2M_MIN'] = df_country['T2M_MIN'] + config['T_offset']
        
        # Precipitation (can't be negative)
        df_country['PRECTOTCORR'] = df_country['PRECTOTCORR'] * config['P_multiplier']
        
        df_country['Country'] = country
        
        out_path = f"../data/{country.lower()}_clean.csv"
        df_country.to_csv(out_path)
        print(f"Saved to {out_path}")

if __name__ == "__main__":
    generate_mock_datasets()
