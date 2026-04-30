import pandas as pd
import os
import glob

def load_data():
    """
    Load and concatenate all clean datasets from the data folder.
    """
    path_pattern = os.path.join(os.path.dirname(__file__), '..', 'data', '*_clean.csv')
    files = glob.glob(path_pattern)
    
    if not files:
        # Fallback if no files exist
        return pd.DataFrame()
        
    df_list = []
    for file in files:
        temp_df = pd.read_csv(file, parse_dates=['Date'])
        df_list.append(temp_df)
        
    df_all = pd.concat(df_list, ignore_index=True)
    df_all['Year'] = df_all['Date'].dt.year
    return df_all
