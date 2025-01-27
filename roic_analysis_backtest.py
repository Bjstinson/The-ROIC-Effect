import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Define tickers to backtest
tickers = ["META", "AAPL", "MSFT", "GOOGL"]  # Add more tickers as needed
roic_threshold = 10  # Define the ROIC threshold

# Initialize a list to store results
results = []

# Backtest each ticker
for ticker in tickers:
    stock = yf.Ticker(ticker)

    # Fetch financial data
    income_statement = stock.financials
    balance_sheet = stock.balance_sheet
    history = stock.history(period="5y")  # 5 years of stock price data

    # Calculate ROIC for the last 3 years
    try:
        roic_data = []
        for year in income_statement.columns[-3:]:  # Last 3 years
            operating_income = income_statement.loc["Operating Income", year]
            invested_capital = balance_sheet.loc["Invested Capital", year]
            roic = (operating_income / invested_capital) * 100
            roic_data.append(roic)

        # Check if ROIC > threshold for 3 consecutive years
        if all(roic > roic_threshold for roic in roic_data):
            # Calculate price performance (1-year, 3-year, 5-year returns)
            start_price = history["Close"].iloc[-252]  # ~1 year ago
            end_price = history["Close"].iloc[-1]  # Most recent price
            one_year_return = (end_price - start_price) / start_price * 100

            three_year_return = None
            if len(history) >= 252 * 3:
                three_year_return = (
                    history["Close"].iloc[-1] - history["Close"].iloc[-252 * 3]
                ) / history["Close"].iloc[-252 * 3] * 100

            # Append results
            results.append(
                {
                    "Ticker": ticker,
                    "1-Year Return (%)": one_year_return,
                    "3-Year Return (%)": three_year_return,
                    "ROIC Data": roic_data,
                }
            )

    except KeyError as e:
        print(f"Data missing for {ticker}: {e}")
        continue

# Convert results to a DataFrame
results_df = pd.DataFrame(results)

# Plot 1: Bar Chart for Stock Returns
plt.figure(figsize=(10, 6))
sns.barplot(
    data=results_df.melt(
        id_vars=["Ticker"], value_vars=["1-Year Return (%)", "3-Year Return (%)"]
    ),
    x="Ticker",
    y="value",
    hue="variable",
)
plt.title("Stock Returns for Companies with ROIC > 10% for 3 Years", fontsize=14)
plt.ylabel("Return (%)", fontsize=12)
plt.xlabel("Company", fontsize=12)
plt.legend(title="Time Period")
plt.grid(axis="y", linestyle="--", alpha=0.6)
plt.show()

# Plot 2: Line Graph for ROIC Trends
plt.figure(figsize=(12, 6))
for idx, row in results_df.iterrows():
    plt.plot(
        ["Year -3", "Year -2", "Year -1"], row["ROIC Data"], marker="o", label=row["Ticker"]
    )
plt.title("ROIC Trends Over the Last 3 Years", fontsize=14)
plt.ylabel("ROIC (%)", fontsize=12)
plt.xlabel("Years", fontsize=12)
plt.axhline(y=roic_threshold, color="red", linestyle="--", label="ROIC Threshold (10%)")
plt.legend(title="Company")
plt.grid(alpha=0.6)
plt.show()

# Display Results Table
print("\nResults Table:")
print(results_df)

# Highlight the table (optional for Jupyter Notebooks)
try:
    from tabulate import tabulate

    print(tabulate(results_df, headers="keys", tablefmt="fancy_grid"))
except ImportError:
    print(results_df)
