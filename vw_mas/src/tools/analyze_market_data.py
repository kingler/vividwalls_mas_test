from langchain.tools import tool
import pandas as pd
import statsmodels.api as sm

@tool("Perform analytics")
class AnalyticsTool

    def analyze_market_data(data):
        """
        Conducts comprehensive market data analysis including descriptive statistics,
        trend analysis, and simple linear regression to identify relationships and
        forecast potential future trends.

        Parameters:
        - data (pd.DataFrame): A DataFrame containing the market data with columns like 'date' and 'value'

        Returns:
        - str: A summary of the analysis results.
        """
        if data.empty:
            return "No data available for analysis."
        
        # Ensure data types are correct, 'date' should be datetime type and 'value' should be numeric
        data['date'] = pd.to_datetime(data['date'])
        data['value'] = pd.to_numeric(data['value'], errors='coerce')
        
        # Dropping rows where 'value' might be NaN after conversion
        data.dropna(subset=['value'], inplace=True)

        # Descriptive statistics
        descriptive_stats = data['value'].describe()
        
        # Trend analysis using time series decomposition
        decomposition = sm.tsa.seasonal_decompose(data.set_index('date')['value'], model='additive', period=12)
        trend = decomposition.trend.dropna()  # Dropping NaN values which are common at the start/end of the series

        # Simple linear regression to forecast future values
        data['time'] = range(len(data))  # Adding a time variable for regression
        model = sm.OLS(data['value'], sm.add_constant(data['time'])).fit()
        forecast_next_period = model.predict({'const': 1, 'time': len(data)})[0]

        # Compile analysis results into a summary
        analysis_summary = (
            f"Descriptive Statistics:\n{descriptive_stats}\n\n"
            f"Trend Analysis (Sample from Middle of Dataset):\n{trend[trend.size//2-5:trend.size//2+5]}\n\n"
            f"Forecast for Next Period Based on Linear Regression: {forecast_next_period:.2f}"
        )

        return analysis_summary
