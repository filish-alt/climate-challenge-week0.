# Scripts

This directory contains utility scripts for data generation and processing.

## generate_mock_data.py
This script takes the baseline `data/ethiopia.csv` file and generates cleaned, synthetic datasets for 5 countries (Ethiopia, Kenya, Somalia, Sudan, Djibouti) by applying realistic offsets to temperature and precipitation variables.

**Usage:**
```bash
python scripts/generate_mock_data.py
```
This will populate the `data/` folder with `_clean.csv` files for each country.

## Streamlit Dashboard
The dashboard application is located in the `app/` directory.

**Usage:**
```bash
streamlit run app/main.py
```
It features a country multi-select, a year range slider, and dynamic charts for temperature trends and precipitation distributions.
