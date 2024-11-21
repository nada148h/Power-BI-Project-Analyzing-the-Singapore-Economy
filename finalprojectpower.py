# -*- coding: utf-8 -*-
"""finalprojectpower.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1mKz_nMtukuGlD13DOztaPMLdgcRSQN0R
"""

from google.colab import files
uploaded = files.upload()

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load the datasets into pandas DataFrames
manpower = pd.read_csv('GovernmentManpower.csv')
revenue = pd.read_csv('GovernmentOperatingRevenue.csv')
fiscal_position = pd.read_csv('GovernmentFiscalPosition.csv')


# Display the first few rows to ensure they loaded correctly
print("Manpower Data:")
print(manpower.head())

print("\nRevenue Data:")
print(revenue.head())

print("\nFiscal Position Data:")
print(fiscal_position.head())

expenditure_df = pd.read_csv('GovernmentExpenditurebyType.csv')
total_expenditure_df = pd.read_csv('GovernmentTotalExpenditure (1).csv')

print("Expenditure Data:")
print(expenditure_df.head())

print("\nTotal Expenditure Data:")
print(total_expenditure_df.head())



"""#Initial Data Cleaning
1. Inspect for Missing Values and Data **Types**
"""

# Check for missing values
print("\nMissing Values in Manpower Data:")
print(manpower.isnull().sum())

print("\nMissing Values in Revenue Data:")
print(revenue.isnull().sum())

print("\nMissing Values in Fiscal Position Data:")
print(fiscal_position.isnull().sum())

# Check data types to ensure consistency
print("\nData Types in Manpower Data:")
print(manpower.dtypes)
# Check for missing values
print(expenditure_df.isnull().sum())
print(total_expenditure_df.isnull().sum())



"""#2. Standardize Column Names"""

# Make column names lowercase and replace spaces with underscores
manpower.columns = manpower.columns.str.lower().str.replace(' ', '_')
revenue.columns = revenue.columns.str.lower().str.replace(' ', '_')
fiscal_position.columns = fiscal_position.columns.str.lower().str.replace(' ', '_')

"""#Handle Missing Values

Drop or fill missing data where needed.
"""

manpower = manpower.dropna()  # Drop missing rows (or use fillna() to fill)
revenue = revenue.fillna(0)  # Example: Fill missing revenue with 0
fiscal_position = fiscal_position.fillna(0)

#Convert Year Columns to Date Format (if needed):
manpower.rename(columns={'financial_year': 'year'}, inplace=True)
revenue.rename(columns={'financial_year': 'year'}, inplace=True)
fiscal_position.rename(columns={'year_of_balance': 'year'}, inplace=True)

print("Manpower Data Columns:", manpower.columns)
print("Revenue Data Columns:", revenue.columns)
print("Fiscal Position Data Columns:", fiscal_position.columns)



"""#Visualization

#1-Government Manpower Insights Visualizations
"""

#Plot Total Government Employees Over Time
total_employees = manpower.groupby('year')['number'].sum()

plt.figure(figsize=(10, 6))
sns.lineplot(data=total_employees, marker='o')
plt.title('Total Government Employees Over Time')
plt.xlabel('Year')
plt.ylabel('Number of Employees')
plt.grid(True)
plt.show()

#Manpower Distribution Across Ministries
latest_year = manpower['year'].max()
manpower_latest = manpower[manpower['year'] == latest_year]

plt.figure(figsize=(12, 7))
sns.barplot(data=manpower_latest, x='ministry', y='number')
plt.title(f'Manpower Distribution Across Ministries ({latest_year})') # Changed this line
plt.xticks(rotation=45, ha='right')
plt.show()

#Trends in Key Ministries Over Time
key_ministries = ['Health', 'Education', 'Defense']
key_ministry_data = manpower[manpower['ministry'].isin(key_ministries)]

plt.figure(figsize=(12, 6))
sns.lineplot(data=key_ministry_data, x='year', y='number', hue='ministry', marker='o')
plt.title('Manpower Trends in Key Ministries')
plt.show()

# 2. Manpower distribution across various ministries
ministry_distribution = manpower.groupby('ministry')['number'].sum().reset_index()
# Plot the distribution of manpower across ministries
plt.figure(figsize=(10, 8))
sns.barplot(x='number', y='ministry', data=ministry_distribution.sort_values('number', ascending=False))
plt.title('Manpower Distribution Across Ministries')
plt.xlabel('Number of Employees')
plt.ylabel('Ministry')
plt.show()



"""#Government Operating Revenue Analysis"""

#total Government Revenue Over Time
total_revenue = revenue.groupby('year')['amount'].sum()

plt.figure(figsize=(10, 6))
sns.lineplot(data=total_revenue, marker='o')
plt.title('Total Government Revenue Over Time')
plt.xlabel('Year')
plt.ylabel('Total Revenue')
plt.grid(True)
plt.show()



# Bar Chart of Revenue Categories by Year
# Check if 'financial_year' is in the columns, if not, use 'year' instead
group_column = 'financial_year' if 'financial_year' in revenue.columns else 'year'

revenue_by_category = revenue.groupby([group_column, 'class'])['amount'].sum().unstack()

revenue_by_category.plot(kind='bar', stacked=True, figsize=(12, 7))
plt.title('Revenue by Category Over Time')
plt.xlabel(group_column.replace('_', ' ').title()) # Format the x-axis label
plt.ylabel('Amount')
plt.legend(title='Category', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.show()

#Top Revenue Contributors Annually
top_revenue_contributors = revenue.groupby('class')['amount'].sum().nlargest(5)

plt.figure(figsize=(10, 6))
sns.barplot(x=top_revenue_contributors.index, y=top_revenue_contributors.values)
plt.title('Top Revenue Contributors')
plt.show()

"""#Fiscal Position Overview"""

#Government Fiscal Balance Over Time
plt.figure(figsize=(10, 6))
# Check if 'basic_balance' is a column in fiscal_position
print(fiscal_position.columns)  # Print columns to check for 'basic_balance'

print(fiscal_position.columns)

print(fiscal_position['item'].unique())
print(fiscal_position['category'].unique())

print(fiscal_position.columns)

# Filter the DataFrame to focus on the relevant fiscal balance item
fiscal_balance = fiscal_position[fiscal_position['item'] == 'Basic Balance']

# Plot the filtered data
plt.figure(figsize=(10, 6))
sns.lineplot(data=fiscal_balance, x='year', y='amount', marker='o')
plt.title('Fiscal Balance Over Time')
plt.xlabel('Year')
plt.ylabel('Amount')
plt.grid(True)
plt.show()

# Aggregate amount by year and item (for a general fiscal overview)
aggregated_fiscal = fiscal_position.groupby(['year', 'item'])['amount'].sum().reset_index()

# Plot fiscal trends for all items
plt.figure(figsize=(12, 7))
sns.lineplot(data=aggregated_fiscal, x='year', y='amount', hue='item', marker='o')
plt.title('Fiscal Trends by Item Over Time')
plt.xlabel('Year')
plt.ylabel('Amount')
plt.legend(title='Item', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True)
plt.show()

# Filter for Revenue and Expenditure categories
revenue_data = fiscal_position[fiscal_position['category'] == 'Revenue']
expenditure_data = fiscal_position[fiscal_position['category'] == 'Expenditure']

# Plot Revenue vs Expenditure trends
plt.figure(figsize=(12, 6))
sns.lineplot(data=revenue_data, x='year', y='amount', label='Revenue', marker='o')
sns.lineplot(data=expenditure_data, x='year', y='amount', label='Expenditure', marker='o')
plt.title('Revenue vs Expenditure Trends Over Time')
plt.xlabel('Year')
plt.ylabel('Amount')
plt.legend(loc='upper left')
plt.grid(True)
plt.show()

# Display the fiscal balance Series
print(fiscal_balance)

# Check the data type of the fiscal balance Series
print(fiscal_balance.dtypes)

# Display the fiscal balance variable
print(fiscal_balance)

# Filter for Expenditure categories
expenditure = fiscal_position[fiscal_position['category'] == 'Expenditure']

# Plot the trends for different items under expenditure
plt.figure(figsize=(12, 7))
sns.lineplot(data=expenditure, x='year', y='amount', hue='item', marker='o')
plt.title('Growth in Expenditure by Category Over Time')
plt.xlabel('Year')
plt.ylabel('Expenditure Amount')
plt.legend(title='Item', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True)
plt.show()

# Filter for Revenue categories and aggregate by year and item
revenue = fiscal_position[fiscal_position['category'] == 'Revenue']
revenue_grouped = revenue.groupby(['year', 'item'])['amount'].sum().reset_index()

# Plot revenue trends by item
plt.figure(figsize=(12, 7))
sns.lineplot(data=revenue_grouped, x='year', y='amount', hue='item', marker='o')
plt.title('Major Revenue Sources Over Time')
plt.xlabel('Year')
plt.ylabel('Revenue Amount')
plt.legend(title='Revenue Type', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True)
plt.show()

# Merge manpower and fiscal data for correlation analysis
merged_data = pd.merge(manpower, fiscal_position, on='year', how='inner')

# Plot correlation between employees and expenditure
plt.figure(figsize=(8, 6))
sns.scatterplot(data=merged_data, x='number', y='amount', hue='item')
plt.title('Correlation Between Employees and Expenditure')
plt.xlabel('Number of Employees')
plt.ylabel('Expenditure Amount')
plt.grid(True)
plt.show()

# Aggregate revenue and expenditure by year
revenue_sum = revenue.groupby('year')['amount'].sum()
expenditure_sum = expenditure.groupby('year')['amount'].sum()

# Calculate the deficit or surplus
fiscal_summary = pd.DataFrame({'revenue': revenue_sum, 'expenditure': expenditure_sum})
fiscal_summary['deficit'] = fiscal_summary['expenditure'] - fiscal_summary['revenue']

# Plot the years where expenditure exceeded revenue
deficit_years = fiscal_summary[fiscal_summary['deficit'] > 0]

plt.figure(figsize=(10, 6))
sns.barplot(x=deficit_years.index, y=deficit_years['deficit'], palette='Reds')
plt.title('Years Where Expenditure Exceeded Revenue')
plt.xlabel('Year')
plt.ylabel('Deficit Amount')
plt.xticks(rotation=45)
plt.show()

# Calculate year-over-year changes in revenue and fiscal balance
fiscal_position['revenue_change'] = fiscal_position['amount'].pct_change()

# Plot the impact of revenue changes on fiscal balance
plt.figure(figsize=(10, 6))
sns.lineplot(data=fiscal_position, x='year', y='revenue_change', marker='o')
plt.title('Impact of Revenue Changes on Fiscal Balance')
plt.xlabel('Year')
plt.ylabel('Revenue Change (YoY)')
plt.grid(True)
plt.show()

# Summing up total expenditure by financial year in total_expenditure_df
total_expenditure_per_year = total_expenditure_df.groupby('financial_year')['amount'].sum()

# Plotting the total expenditure over time
import matplotlib.pyplot as plt

plt.figure(figsize=(10,6))
plt.plot(total_expenditure_per_year.index, total_expenditure_per_year.values)
plt.title('Total Government Expenditure Over Time')
plt.xlabel('Financial Year')
plt.ylabel('Expenditure (Amount)')
plt.grid(True)
plt.show()

# Summing expenditure by type for a specific year or overall
expenditure_by_type = expenditure_df.groupby('type')['amount'].sum()

# Plotting the expenditure by type
expenditure_by_type.plot(kind='bar', figsize=(10,6))
plt.title('Government Expenditure by Type')
plt.xlabel('Expenditure Type')
plt.ylabel('Amount')
plt.grid(True)
plt.show()

#  compare specific types over time
expenditure_by_year_and_type = expenditure_df.groupby(['financial_year', 'type'])['amount'].sum().unstack()

# Plot the expenditure by type over time
expenditure_by_year_and_type.plot(kind='line', figsize=(12,8))
plt.title('Government Expenditure by Type Over Time')
plt.xlabel('Financial Year')
plt.ylabel('Expenditure (Amount)')
plt.grid(True)
plt.show()

# Calculating the year-over-year growth rate
total_expenditure_per_year = total_expenditure_df.groupby('financial_year')['amount'].sum()
yoy_growth = total_expenditure_per_year.pct_change() * 100

# Plotting the Year-over-Year (YoY) growth rate
plt.figure(figsize=(10,6))
plt.plot(yoy_growth.index, yoy_growth.values, marker='o', color='g')
plt.title('Year-over-Year Growth in Government Expenditure')
plt.xlabel('Financial Year')
plt.ylabel('Growth Rate (%)')
plt.grid(True)
plt.show()

# Filtering the most recent year, and then grouping by ministry
latest_year = total_expenditure_df['financial_year'].max()
expenditure_by_ministry = total_expenditure_df[total_expenditure_df['financial_year'] == latest_year].groupby('ministry')['amount'].sum()

# Plotting as a pie chart
expenditure_by_ministry.plot(kind='pie', autopct='%1.1f%%', figsize=(8,8))
plt.title(f'Expenditure Distribution by Ministry for {latest_year}')
plt.ylabel('')  # Hides the 'y' label for pie chart
plt.show()
