# Ensure required libraries are installed: pandas, numpy, matplotlib, seaborn, plotly, geopandas, folium
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium

# Define dataset URL
URL_CASES = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/main/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"

# Load data
df_cases = pd.read_csv(URL_CASES)

# Preview data structure
print("Dataset Overview:")
print(df_cases.head())
print(df_cases.info())


# Data Cleaning and processing
# Remove latitude & longitude columns
df_cases = df_cases.drop(columns=["Lat", "Long"])

# Aggregate data by country
df_cases = df_cases.groupby("Country/Region").sum()

# Transpose for time-series analysis
df_cases = df_cases.T
df_cases.index = pd.to_datetime(df_cases.index)

# Display transformed data
print(df_cases.head())


# Exploratory Data Analysis (EDA)
# Global Trend Analysis
plt.figure(figsize=(12, 6))
df_cases.sum(axis=1).plot(color="blue", linewidth=2)
plt.title("Global COVID-19 Cases Over Time")
plt.xlabel("Date")
plt.ylabel("Total Cases")
plt.grid(True)
plt.show()

# Compare Countries
top_countries = df_cases.iloc[-1].nlargest(5).index

plt.figure(figsize=(12, 6))
for country in top_countries:
    df_cases[country].plot(label=country)

plt.title("Top 5 Countries by COVID-19 Cases")
plt.xlabel("Date")
plt.ylabel("Total Cases")
plt.legend()
plt.grid(True)
plt.show()

# Visualize Data
plt.figure(figsize=(10, 5))
sns.histplot(df_cases.iloc[-1], bins=30, kde=True)
plt.title("Distribution of COVID-19 Cases Across Countries")
plt.xlabel("Cases")
plt.ylabel("Frequency")
plt.show()

# Geospatial mapping
# Initialize world map
world_map = folium.Map(location=[0, 0], zoom_start=2)

# Load latest case counts
latest_data = df_cases.iloc[-1]

# Add country markers with case numbers
for country, cases in latest_data.items():
    folium.Marker(
        location=[0, 0],  # Replace with actual country coordinates if available
        popup=f"{country}: {cases:,} cases",
        icon=folium.Icon(color="red")
    ).add_to(world_map)

# Display map
world_map

# Export Processed Data
df_cases.to_csv("COVID19_Global_Analysis.csv")