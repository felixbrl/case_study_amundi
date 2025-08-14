import pandas as pd
import plotly.express as px
import os
import numpy as np

# --- Column Names ---
COL_EQUITY = 'Equity'
COL_RETURN_1Y = '1 Year Total Return - Previous'
COL_VOL_360D = 'Volatility 360 Day Calc'
COL_PE_BEST = 'BEst P/E Ratio'
COL_VOL_IMPLIED_12M = '12 Month Put Implied Volatility'
COL_PE_AVG_5Y = 'Price / Earnings - 5 Year Average'
COL_LTG_EPS = 'BEst LTG EPS'
COL_UPSIDE = 'Upside with Target Price from Analyst (in %)'
COL_SCORE_1 = 'M Score'
COL_SECTOR_1 = 'Sector (1)'
COL_SECTOR_2 = 'Sector (2)'
COL_RISK_COUNTRY = 'Risk Country'

NUMERIC_COLS = [
    COL_RETURN_1Y, COL_VOL_360D, COL_PE_BEST, COL_VOL_IMPLIED_12M,
    COL_PE_AVG_5Y, COL_LTG_EPS, COL_UPSIDE, COL_SCORE_1
]

def load_data(file_path="data.csv"):
    """Loads and preprocesses the data from the CSV file."""
    try:
        df = pd.read_csv(file_path, sep=';', decimal='.')
        for col in NUMERIC_COLS:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        return df
    except FileNotFoundError:
        print(f"ERROR: File not found at '{file_path}'. Please check the path.")
        return None
    except Exception as e:
        print(f"An error occurred while reading the CSV file: {e}")
        return None

def plot_top_20_returns(df):
    """Generates an interactive plot for Top 20 1-Year Returns."""
    if df is None or COL_EQUITY not in df.columns or COL_RETURN_1Y not in df.columns:
        return None

    data_to_plot = df[[COL_EQUITY, COL_RETURN_1Y]].dropna(subset=[COL_RETURN_1Y]).sort_values(by=COL_RETURN_1Y, ascending=False).head(20)

    if not data_to_plot.empty:
        fig = px.bar(data_to_plot,
                     x=COL_RETURN_1Y,
                     y=COL_EQUITY,
                     orientation='h',
                     title="Top 20 1-Year Returns",
                     labels={COL_RETURN_1Y: "1-Year Return (%)", COL_EQUITY: "Equity"},
                     color=COL_RETURN_1Y,
                     color_continuous_scale=px.colors.sequential.Viridis)
        fig.update_layout(yaxis={'categoryorder':'total ascending'})
        return fig
    return None

def plot_top_20_upside_potential(df):
    """Generates an interactive plot for Top 20 Upside Potential."""
    data_to_plot = df[[COL_EQUITY, COL_UPSIDE]].dropna(subset=[COL_UPSIDE]).sort_values(by=COL_UPSIDE, ascending=False).head(20)
    fig = px.bar(data_to_plot, x=COL_UPSIDE, y=COL_EQUITY, orientation='h', title="Top 20 Upside Potential (Analysts)", labels={COL_UPSIDE: "Upside Potential (%)", COL_EQUITY: "Equity"}, color=COL_UPSIDE, color_continuous_scale=px.colors.sequential.Mako)
    fig.update_layout(yaxis={'categoryorder':'total ascending'})
    return fig

def plot_distribution_of_returns(df):
    """Generates an interactive plot for the distribution of 1-Year Returns."""
    data_to_plot = df[COL_RETURN_1Y].dropna()
    fig = px.histogram(data_to_plot, x=COL_RETURN_1Y, title="Distribution of 1-Year Returns", labels={COL_RETURN_1Y: "1-Year Return (%)"}, marginal="box")
    return fig

def plot_distribution_of_upside_potential(df):
    """Generates an interactive plot for the distribution of Upside Potential."""
    data_to_plot = df[COL_UPSIDE].dropna()
    fig = px.histogram(data_to_plot, x=COL_UPSIDE, title="Distribution of Upside Potential", labels={COL_UPSIDE: "Upside Potential (%)"}, marginal="box", color_discrete_sequence=['salmon'])
    return fig

def plot_return_vs_volatility(df):
    """Generates an interactive scatter plot of Return vs. Volatility."""
    data_to_plot = df[[COL_RETURN_1Y, COL_VOL_360D, COL_SECTOR_1, COL_EQUITY]].dropna(subset=[COL_RETURN_1Y, COL_VOL_360D])
    fig = px.scatter(data_to_plot, x=COL_VOL_360D, y=COL_RETURN_1Y, color=COL_SECTOR_1, title="Return vs. Volatility", labels={COL_VOL_360D: "360-Day Volatility (%)", COL_RETURN_1Y: "1-Year Return (%)"}, hover_data=[COL_EQUITY])
    return fig

def plot_average_performance_by_sector(df):
    """Generates an interactive bar chart of Average Performance by Sector."""
    sector_performance = df.groupby(COL_SECTOR_1)[COL_RETURN_1Y].mean().dropna().sort_values(ascending=False).reset_index()
    fig = px.bar(sector_performance, x=COL_SECTOR_1, y=COL_RETURN_1Y, title="Average Performance by Sector", labels={COL_SECTOR_1: "Sector", COL_RETURN_1Y: "Average 1-Year Return (%)"}, color=COL_SECTOR_1)
    return fig

def plot_sharpe_ratio(df):
    """Generates an interactive bar chart of Top 20 equities by Sharpe Ratio."""
    risk_free_rate = 3.0
    # Replace 0 volatility with NaN to avoid division by zero
    df['Sharpe Volatility for Calc'] = df[COL_VOL_360D].replace(0, np.nan)
    df['Sharpe Ratio'] = (df[COL_RETURN_1Y] - risk_free_rate) / df['Sharpe Volatility for Calc']
    # Replace infinite values with NaN
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    
    data_to_plot = df[[COL_EQUITY, 'Sharpe Ratio']].dropna(subset=['Sharpe Ratio']).sort_values(by='Sharpe Ratio', ascending=False).head(20)
    
    fig = px.bar(data_to_plot, x='Sharpe Ratio', y=COL_EQUITY, orientation='h', title=f"Top 20 Equities by Sharpe Ratio (Rf={risk_free_rate}%)", labels={'Sharpe Ratio': f"Sharpe Ratio (Rf={risk_free_rate}%)", COL_EQUITY: "Equity"}, color='Sharpe Ratio', color_continuous_scale=px.colors.diverging.RdYlGn)
    fig.update_layout(yaxis={'categoryorder':'total ascending'})
    
    # Clean up temporary column
    df.drop(columns=['Sharpe Volatility for Calc'], inplace=True)

    return fig

AVAILABLE_PLOTS = {
    "Top 20 1-Year Returns": plot_top_20_returns,
    "Top 20 Upside Potential (Analysts)": plot_top_20_upside_potential,
    "Distribution of 1-Year Returns": plot_distribution_of_returns,
    "Distribution of Upside Potential": plot_distribution_of_upside_potential,
    "Return vs. Volatility": plot_return_vs_volatility,
    "Average Performance by Sector": plot_average_performance_by_sector,
    "Top 20 Equities by Sharpe Ratio": plot_sharpe_ratio,
}