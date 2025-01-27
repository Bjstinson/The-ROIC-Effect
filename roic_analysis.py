import yfinance as yf
import pandas as pd

# Fetch financial data for a company
ticker = "META"  # Replace with your desired stock ticker
stock = yf.Ticker(ticker)

# Retrieve financial statements
income_statement = stock.financials  # Operating Income
balance_sheet = stock.balance_sheet  # Invested Capital is here

# Set the tax rate
tax_rate = 0.21  # Example: 21% tax rate

# Initialize variables to store results
roic_data = []

# Get the last 3 years available in the financial statements
available_years = income_statement.columns[-4:]  # Select the last 4 years

# Loop through the selected years
for year in available_years:
    try:
        # Fetch Operating Income
        operating_income = income_statement.loc["Operating Income", year]

        # Fetch Invested Capital directly
        invested_capital = balance_sheet.loc["Invested Capital", year]

        # Calculate NOPAT
        nopat = operating_income * (1 - tax_rate)

        # Calculate ROIC
        roic = (nopat / invested_capital) * 100
        roic_data.append({"Year": year, "ROIC (%)": roic})

    except KeyError as e:
        print(f"Missing data for year {year}: {e}")
        roic_data.append({"Year": year, "ROIC (%)": None})

# Convert results to a DataFrame
roic_df = pd.DataFrame(roic_data)

# Calculate the average ROIC for the last 3 years
valid_roic_values = roic_df["ROIC (%)"].dropna()  # Exclude missing data
average_roic = valid_roic_values.mean()

# Print results
print("\nROIC Data for the Last 3 Years:")
print(roic_df)
print(f"\nAverage ROIC for the Last 3 Years: {average_roic:.2f}%")



