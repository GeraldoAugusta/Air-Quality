# Air Quality Data Analysis Dashboard

## Project Overview

This project analyzes air quality data in Beijing using exploratory data
analysis (EDA) and presents the insights through an interactive
Streamlit dashboard.

The dataset contains measurements of several air pollutants such as
PM2.5, PM10, SO2, NO2, CO, and O3, along with meteorological variables
like temperature, pressure, wind direction, and rainfall.

The objective of the analysis is to understand patterns of air pollution
over time and compare air quality levels across monitoring stations.

------------------------------------------------------------------------

## Business Questions

1.  How does air pollution (especially PM2.5 and PM10) change over time?
2.  Which monitoring stations record the highest and lowest air
    pollution levels?

------------------------------------------------------------------------

## Project Structure

submission │ ├── dashboard │ ├── main_data.csv │ └── dashboard.py │ ├──
data │ ├── data_1.csv │ └── data_2.csv │ ├── notebook.ipynb ├──
README.md ├── requirements.txt └── url.txt

------------------------------------------------------------------------

## Data Analysis Steps

1.  **Data Gathering**
    -   Combining multiple CSV files into one main dataset.
2.  **Data Assessing**
    -   Checking data types, missing values, and duplicates.
3.  **Data Cleaning**
    -   Handling missing values and creating a datetime column for
        time-based analysis.
4.  **Exploratory Data Analysis**
    -   Exploring relationships between air pollutants and identifying
        patterns.
5.  **Data Visualization**
    -   Creating visualizations to show pollution trends and station
        comparisons.

------------------------------------------------------------------------

## Dashboard

The dashboard was built using **Streamlit** to allow interactive
exploration of air quality data.

Dashboard features include: - Filtering data by monitoring station -
Selecting time ranges - Viewing pollution trends over time - Comparing
air quality between stations - Viewing summary metrics such as average
PM2.5 and PM10

------------------------------------------------------------------------

## How to Run the Dashboard

Install dependencies:

pip install -r requirements.txt

Run the dashboard:

streamlit run dashboard/dashboard.py
