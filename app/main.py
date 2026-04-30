import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from utils import load_data

st.set_page_config(page_title="Climate Dashboard", layout="wide")

st.title("Cross-Country Climate Vulnerability Dashboard")
st.markdown("This dashboard visualizes climate metrics across five East African nations to inform COP32 policy.")

# Load Data
@st.cache_data
def get_data():
    return load_data()

df = get_data()

if df.empty:
    st.error("No data found. Please ensure the mock data script has been run.")
    st.stop()

# Sidebar for Filters
st.sidebar.header("Filter Options")

# Country Multi-select
all_countries = df['Country'].unique().tolist()
selected_countries = st.sidebar.multiselect("Select Countries", all_countries, default=all_countries)

# Year Range Slider
min_year = int(df['Year'].min())
max_year = int(df['Year'].max())
selected_years = st.sidebar.slider("Select Year Range", min_year, max_year, (min_year, max_year))

# Variable Selector Dropdown (Bonus)
variables = ["T2M", "PRECTOTCORR", "RH2M", "WS2M"]
selected_var = st.sidebar.selectbox("Select Variable for Trend Chart", variables, index=0)

# Filter Dataset
filtered_df = df[
    (df['Country'].isin(selected_countries)) &
    (df['Year'] >= selected_years[0]) &
    (df['Year'] <= selected_years[1])
]

if filtered_df.empty:
    st.warning("No data matches the selected filters.")
    st.stop()

# Layout
col1, col2 = st.columns(2)

with col1:
    st.subheader(f"Trend Line Chart: {selected_var}")
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    
    # Calculate monthly average for the selected variable
    monthly_avg = filtered_df.groupby(['Country', filtered_df['Date'].dt.to_period('M')])[selected_var].mean().reset_index()
    monthly_avg['Date'] = monthly_avg['Date'].dt.to_timestamp()
    
    sns.lineplot(data=monthly_avg, x='Date', y=selected_var, hue='Country', ax=ax1, linewidth=1.5)
    ax1.set_xlabel("Date")
    ax1.set_ylabel(selected_var)
    plt.tight_layout()
    st.pyplot(fig1)

with col2:
    st.subheader("Precipitation Distribution (Boxplot)")
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    sns.boxplot(data=filtered_df, x='Country', y='PRECTOTCORR', ax=ax2)
    ax2.set_xlabel("Country")
    ax2.set_ylabel("Precipitation (mm)")
    
    # Restrict y-axis to a reasonable percentile so the box is visible
    p95 = filtered_df['PRECTOTCORR'].quantile(0.95)
    if p95 > 0:
        ax2.set_ylim(-1, p95 * 1.5)
    
    plt.tight_layout()
    st.pyplot(fig2)

st.markdown("---")
st.markdown("### Key Observations")
st.markdown("- **Heat Trends**: Sudan consistently exhibits the highest average temperatures.")
st.markdown("- **Precipitation**: Somalia and Djibouti experience very minimal rain, making them highly vulnerable to droughts.")
st.markdown("- **Ethiopia**: Has a moderate temperature due to highland elevation but faces variable precipitation.")
