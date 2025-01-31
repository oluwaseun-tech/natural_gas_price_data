import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os

# URL of the page that contains the Excel file
url = 'https://www.eia.gov/dnav/ng/hist/rngwhhdM.htm'

# Send a request to fetch the page content
response = requests.get(url)

# Parse the page using BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Find all links on the page
links = soup.find_all('a')

# Look for the link to the Excel file by checking for the .xls or .xlsx extension
excel_url = None
for link in links:
    href = link.get('href', '')
    if href.endswith('.xls') or href.endswith('.xlsx'):
        # Use urljoin to ensure the URL is complete
        excel_url = urljoin(url, href)
        break

# Check if we found the Excel URL
if excel_url:
    try:
        # Send a request to download the file
        file_response = requests.get(excel_url)
        file_response.raise_for_status()  # Raise an error if the request failed

        # Set the filename
        filename = os.path.basename(excel_url)

        # Save the file locally
        with open(filename, 'wb') as file:
            file.write(file_response.content)
        print(f"File downloaded successfully: {filename}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while downloading the file: {e}")
else:
    print("Excel file not found on the page.")


import os

# Get the current working directory
current_directory = os.getcwd()

# Print the full file path
file_path = os.path.join(current_directory, 'RNGWHHDm.xls')
print(f"File is located at: {file_path}")


import pandas as pd

# Step 1: Read the Excel file
xls_file = r'C:\Users\hp\Downloads\RNGWHHDm.xls'
df = pd.read_excel(xls_file, sheet_name='Data 1', header=1)  # Adjust sheet name if necessary

# Step 2: Clean the data (make sure we only have Date and Price columns)
# Assuming the data has columns 'Date' and 'Price' (you may need to adjust column names based on the actual data)
df.columns = ['Date', 'Price']  # Keep only the 'Date' and 'Price' columns

# Drop the first row, which seems to be metadata
df = df.drop(0)

# Convert 'Date' column to datetime format
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

# Remove rows where 'Date' is NaT
df = df.dropna(subset=['Date'])

# Reset the index
df = df.reset_index(drop=True)

# Step 3: Save daily data to a CSV file
df_daily = df[['Date', 'Price']]  # Make sure the data only includes 'Date' and 'Price'
df_daily.to_csv('daily_natural_gas_prices.csv', index=False)

# Step 4: Generate monthly data (using the first date of each month)
# Assuming the first date of the month should be used for monthly data
df_monthly = df_daily.resample('ME', on='Date').first()

# Reset the index to get 'Date' as a column again
df_monthly = df_monthly.reset_index()

# Format the Date as 'Month Year' (e.g., 'January 1997')
df_monthly['Date'] = df_monthly['Date'].dt.strftime('%B %Y')

# Only keep 'Date' and 'Price' columns
df_monthly = df_monthly[['Date', 'Price']]

# Step 5: Save monthly data to a CSV file
df_monthly.to_csv('monthly_natural_gas_prices.csv', index=False)

print("Data processed and saved to CSV files!")


#Visualization
import matplotlib.pyplot as plt
import pandas as pd

# Load data
df = pd.read_csv('monthly_natural_gas_prices.csv')

# Convert 'Date' to datetime
df['Date'] = pd.to_datetime(df['Date'])

# Create the line plot
plt.figure(figsize=(10,6))
plt.plot(df['Date'], df['Price'], marker='o', color='b', label='Price')
plt.title('Monthly Natural Gas Prices')
plt.xlabel('Date')
plt.ylabel('Price (USD)')
plt.grid(True)
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


from datapackage import Package

# Define the metadata for the data package
package = Package({
    'profile': 'tabular-data-package',
    'name': 'natural-gas-prices',
    'title': 'Natural Gas Prices Data',
    'version': '1.0.0',
    'resources': [
        {
            'name': 'daily-prices',
            'path': 'daily_natural_gas_prices.csv',
            'format': 'csv',
            'schema': {
                'fields': [
                    { 'name': 'Date', 'type': 'date' },
                    { 'name': 'Price', 'type': 'number' }
                ]
            }
        },
        {
            'name': 'monthly-prices',
            'path': 'monthly_natural_gas_prices.csv',
            'format': 'csv',
            'schema': {
                'fields': [
                    { 'name': 'Date', 'type': 'date' },
                    { 'name': 'Price', 'type': 'number' }
                ]
            }
        }
    ]
})

# Save the datapackage.json file
package.save('datapackage.json')