import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import numpy as np # Pour les calculs de moyenne/mediane

# --- Configuration ---
# !!! METTEZ À JOUR CE CHEMIN AVEC L'EMPLACEMENT DE VOTRE FICHIER CSV !!!
file_path_csv = r"D:\Téléchargements\Privé_ Exercices pour l'entretien du Stage Assistant Gestion Multi Asset\data.csv"
output_dir = r"D:\Téléchargements\Privé_ Exercices pour l'entretien du Stage Assistant Gestion Multi Asset\rapport"

# Créer le répertoire de sortie s'il n'existe pas
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# --- Définition des noms de colonnes (ajuster si nécessaire) ---
col_equity = 'Equity'
col_return_1y = '1 Year Total Return - Previous'
col_vol_360d = 'Volatility 360 Day Calc'
col_pe_best = 'BEst P/E Ratio'
col_vol_implied_12m = '12 Month Put Implied Volatility'
col_pe_avg_5y = 'Price / Earnings - 5 Year Average'
col_ltg_eps = 'BEst LTG EPS'
col_upside = 'Upside with Target Price from Analyst (in %)'
col_score_1 = 'M Score'
col_sector_1 = 'Sector (1)'
col_sector_2 = 'Sector (2)'
col_risk_country = 'Risk Country'

# Liste des colonnes numériques à convertir
numeric_cols = [
    col_return_1y, col_vol_360d, col_pe_best, col_vol_implied_12m,
    col_pe_avg_5y, col_ltg_eps, col_upside, col_score_1
]

# --- Data Loading and Preparation ---
try:
    df = pd.read_csv(file_path_csv, sep=';', decimal='.')
except FileNotFoundError:
    print(f"ERROR: File not found at '{file_path_csv}'. Please check the path.")
    exit()
except Exception as e:
    print(f"An error occurred while reading the CSV file: {e}")
    exit()

# Adjust actual column names if they differ slightly from definitions
# For example, if 'Volatility 360 Day Calc' is the actual name in CSV for col_vol_360d
# This script will use the variables above. Ensure they match your CSV headers *exactly*.
# Example: if CSV has 'Volatility 360 Day Calc', then col_vol_360d should be = 'Volatility 360 Day Calc'

# Numeric conversion (assuming data is clean as per your manual edit, but this is good practice)
for col in numeric_cols:
    if col in df.columns:
        # If your CSV was manually cleaned, values might already be numeric.
        # If not, and they were like "12.3%", the cleaning for '%' would be needed here.
        # Since you confirmed manual cleaning worked, we expect to_numeric to succeed.
        df[col] = pd.to_numeric(df[col], errors='coerce')
    else:
        print(f"WARNING: Column '{col}' defined in numeric_cols is not found in the CSV file.")

# Function to save and close plots
def save_and_close_plot(fig, title_en):
    fig.suptitle(title_en, fontsize=16)
    plt.tight_layout(rect=[0, 0, 1, 0.96]) 
    file_name = "".join(c if c.isalnum() else "_" for c in title_en) + ".png"
    fig.savefig(os.path.join(output_dir, file_name))
    plt.close(fig)
    print(f"Chart saved: {file_name}")

# --- Chart Generation (with English titles and labels) ---

# 1. Top 20 1-Year Returns
if col_equity in df.columns and col_return_1y in df.columns:
    data_to_plot = df[[col_equity, col_return_1y]].dropna(subset=[col_return_1y]).sort_values(by=col_return_1y, ascending=False).head(20)
    if not data_to_plot.empty:
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.barplot(x=col_return_1y, y=col_equity, data=data_to_plot, ax=ax, 
                    palette="viridis", hue=col_equity, legend=False)
        ax.set_xlabel("1-Year Return (%)")
        ax.set_ylabel(col_equity) # Uses the direct column name, which is 'Equity'
        save_and_close_plot(fig, "1. Top 20 1-Year Returns")

# 2. Top 20 Upside Potential (Analysts)
if col_equity in df.columns and col_upside in df.columns:
    data_to_plot = df[[col_equity, col_upside]].dropna(subset=[col_upside]).sort_values(by=col_upside, ascending=False).head(20)
    if not data_to_plot.empty:
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.barplot(x=col_upside, y=col_equity, data=data_to_plot, ax=ax, 
                    palette="mako", hue=col_equity, legend=False)
        ax.set_xlabel("Upside Potential (%)")
        ax.set_ylabel(col_equity)
        save_and_close_plot(fig, "2. Top 20 Upside Potential (Analysts)")

# 3. Distribution of 1-Year Returns
if col_return_1y in df.columns:
    data_to_plot = df[col_return_1y].dropna()
    if not data_to_plot.empty:
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.histplot(data_to_plot, kde=True, ax=ax, color="skyblue")
        ax.set_xlabel("1-Year Return (%)")
        ax.set_ylabel("Frequency")
        save_and_close_plot(fig, "3. Distribution of 1-Year Returns")

# 4. Distribution of Upside Potential
if col_upside in df.columns:
    data_to_plot = df[col_upside].dropna()
    if not data_to_plot.empty:
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.histplot(data_to_plot, kde=True, ax=ax, color="salmon")
        ax.set_xlabel("Upside Potential (%)")
        ax.set_ylabel("Frequency")
        save_and_close_plot(fig, "4. Distribution of Upside Potential")

# 5. Top 20 Historical Volatility (360 Days)
if col_equity in df.columns and col_vol_360d in df.columns:
    data_to_plot = df[[col_equity, col_vol_360d]].dropna(subset=[col_vol_360d]).sort_values(by=col_vol_360d, ascending=False).head(20)
    if not data_to_plot.empty:
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.barplot(x=col_vol_360d, y=col_equity, data=data_to_plot, ax=ax, 
                    palette="coolwarm", hue=col_equity, legend=False)
        ax.set_xlabel("360-Day Volatility (%)") # Assuming 'Volatility 360 Day' is the column name in use
        ax.set_ylabel(col_equity)
        save_and_close_plot(fig, "5. Top 20 Historical Volatility (360 Days)")

# 6. Top 20 Implied Volatility (12 Months)
if col_equity in df.columns and col_vol_implied_12m in df.columns:
    data_to_plot = df[[col_equity, col_vol_implied_12m]].dropna(subset=[col_vol_implied_12m]).sort_values(by=col_vol_implied_12m, ascending=False).head(20)
    if not data_to_plot.empty:
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.barplot(x=col_vol_implied_12m, y=col_equity, data=data_to_plot, ax=ax, 
                    palette="plasma", hue=col_equity, legend=False)
        ax.set_xlabel("12-Month Implied Volatility (%)")
        ax.set_ylabel(col_equity)
        save_and_close_plot(fig, "6. Top 20 Implied Volatility (12 Months)")

# 7. Historical vs. Implied Volatility
if col_vol_360d in df.columns and col_vol_implied_12m in df.columns:
    data_to_plot = df[[col_vol_360d, col_vol_implied_12m, col_sector_1 if col_sector_1 in df.columns else col_equity]].dropna(subset=[col_vol_360d, col_vol_implied_12m])
    if not data_to_plot.empty:
        fig, ax = plt.subplots(figsize=(10, 6))
        hue_col_for_scatter = col_sector_1 if col_sector_1 in df.columns and df[col_sector_1].nunique() < 20 else None
        sns.scatterplot(x=col_vol_360d, y=col_vol_implied_12m, data=data_to_plot, ax=ax, 
                        hue=hue_col_for_scatter, legend='brief' if hue_col_for_scatter else False)
        ax.set_xlabel("360-Day Historical Volatility (%)")
        ax.set_ylabel("12-Month Implied Volatility (%)")
        if hue_col_for_scatter: ax.legend(title=col_sector_1, bbox_to_anchor=(1.05, 1), loc='upper left') # Legend title uses column name
        save_and_close_plot(fig, "7. Historical vs. Implied Volatility")

# 8. Top 20 P/E Ratios (BEst)
if col_equity in df.columns and col_pe_best in df.columns:
    data_to_plot = df[[col_equity, col_pe_best]].dropna(subset=[col_pe_best]).sort_values(by=col_pe_best, ascending=False).head(20)
    if not data_to_plot.empty:
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.barplot(x=col_pe_best, y=col_equity, data=data_to_plot, ax=ax, 
                    palette="cubehelix", hue=col_equity, legend=False)
        ax.set_xlabel("P/E Ratio (BEst)")
        ax.set_ylabel(col_equity)
        save_and_close_plot(fig, "8. Top 20 P/E Ratios (BEst)")

# 9. Current P/E vs. 5-Year Average P/E
if col_pe_best in df.columns and col_pe_avg_5y in df.columns:
    data_to_plot = df[[col_equity, col_pe_best, col_pe_avg_5y, col_sector_1 if col_sector_1 in df.columns else col_equity]].dropna(subset=[col_pe_best, col_pe_avg_5y])
    if not data_to_plot.empty:
        fig, ax = plt.subplots(figsize=(10, 6))
        hue_col_for_scatter = col_sector_1 if col_sector_1 in df.columns and df[col_sector_1].nunique() < 20 else None
        sns.scatterplot(x=col_pe_avg_5y, y=col_pe_best, data=data_to_plot, ax=ax, 
                        hue=hue_col_for_scatter, legend='brief' if hue_col_for_scatter else False)
        ax.set_xlabel("5-Year Average P/E")
        ax.set_ylabel("Current P/E (BEst)")
        min_val_x = data_to_plot[col_pe_avg_5y].min()
        max_val_x = data_to_plot[col_pe_avg_5y].max()
        min_val_y = data_to_plot[col_pe_best].min()
        max_val_y = data_to_plot[col_pe_best].max()
        if pd.notna(min_val_x) and pd.notna(max_val_x) and pd.notna(min_val_y) and pd.notna(max_val_y):
            overall_min = min(min_val_x, min_val_y)
            overall_max = max(max_val_x, max_val_y)
            ax.plot([overall_min, overall_max], [overall_min, overall_max], 'k--', lw=2) 
        if hue_col_for_scatter: ax.legend(title=col_sector_1, bbox_to_anchor=(1.05, 1), loc='upper left')
        save_and_close_plot(fig, "9. Current P_E vs 5-Year Average P_E")

# 10. Top 20 Long-Term EPS Growth
if col_equity in df.columns and col_ltg_eps in df.columns:
    data_to_plot = df[[col_equity, col_ltg_eps]].dropna(subset=[col_ltg_eps]).sort_values(by=col_ltg_eps, ascending=False).head(20)
    if not data_to_plot.empty:
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.barplot(x=col_ltg_eps, y=col_equity, data=data_to_plot, ax=ax, 
                    palette="rocket", hue=col_equity, legend=False)
        ax.set_xlabel("Long-Term EPS Growth (BEst LTG EPS %)")
        ax.set_ylabel(col_equity)
        save_and_close_plot(fig, "10. Top 20 Long-Term EPS Growth")

# 11. Return vs. Volatility
if col_return_1y in df.columns and col_vol_360d in df.columns:
    data_to_plot = df[[col_return_1y, col_vol_360d, col_sector_1 if col_sector_1 in df.columns else col_equity]].dropna(subset=[col_return_1y, col_vol_360d])
    if not data_to_plot.empty:
        fig, ax = plt.subplots(figsize=(12, 7))
        hue_col_for_scatter = col_sector_1 if col_sector_1 in df.columns and df[col_sector_1].nunique() < 20 else None
        sns.scatterplot(x=col_vol_360d, y=col_return_1y, data=data_to_plot, 
                        hue=hue_col_for_scatter, ax=ax, legend='brief' if hue_col_for_scatter else False)
        ax.set_xlabel("360-Day Volatility (%)")
        ax.set_ylabel("1-Year Return (%)")
        if hue_col_for_scatter: ax.legend(title=col_sector_1, bbox_to_anchor=(1.05, 1), loc='upper left')
        save_and_close_plot(fig, "11. Return vs. Volatility")

# --- Bar charts using pandas .plot() ---

# 12. Average Performance by Sector (Sector 1)
if col_return_1y in df.columns and col_sector_1 in df.columns:
    sector_performance = df.groupby(col_sector_1)[col_return_1y].mean().dropna().sort_values(ascending=False)
    if not sector_performance.empty:
        fig, ax = plt.subplots(figsize=(12, 7))
        sector_performance.plot(kind='bar', ax=ax, color=sns.color_palette("Set2", len(sector_performance)))
        ax.set_xlabel(f"Sector ({col_sector_1})")
        ax.set_ylabel("Average 1-Year Return (%)")
        plt.xticks(rotation=45, ha="right")
        save_and_close_plot(fig, f"12. Average Performance by {col_sector_1}")

# 13. Average Upside Potential by Sector (Sector 1)
if col_upside in df.columns and col_sector_1 in df.columns:
    sector_upside = df.groupby(col_sector_1)[col_upside].mean().dropna().sort_values(ascending=False)
    if not sector_upside.empty:
        fig, ax = plt.subplots(figsize=(12, 7))
        sector_upside.plot(kind='bar', ax=ax, color=sns.color_palette("Set3", len(sector_upside)))
        ax.set_xlabel(f"Sector ({col_sector_1})")
        ax.set_ylabel("Average Upside Potential (%)")
        plt.xticks(rotation=45, ha="right")
        save_and_close_plot(fig, f"13. Average Upside Potential by {col_sector_1}")

# 14. Number of Equities by Risk Country
if col_risk_country in df.columns:
    country_counts = df[col_risk_country].value_counts().dropna()
    if not country_counts.empty:
        fig, ax = plt.subplots(figsize=(10, 7))
        country_counts.plot(kind='bar', ax=ax, color=sns.color_palette("Paired", len(country_counts)))
        ax.set_xlabel("Risk Country")
        ax.set_ylabel("Number of Equities")
        plt.xticks(rotation=45, ha="right")
        save_and_close_plot(fig, "14. Number of Equities by Risk Country")

# 15. Average Score by Sector ({col_sector_1})
if col_score_1 in df.columns and col_sector_1 in df.columns:
    sector_score = df.groupby(col_sector_1)[col_score_1].mean().dropna().sort_values(ascending=False)
    if not sector_score.empty:
        fig, ax = plt.subplots(figsize=(12, 7))
        sector_score.plot(kind='bar', ax=ax, color=sns.color_palette("tab10", len(sector_score)))
        ax.set_xlabel(f"Sector ({col_sector_1})")
        ax.set_ylabel(f"Average Score ({col_score_1})") # Uses column name for score, e.g. 'M Score'
        plt.xticks(rotation=45, ha="right")
        save_and_close_plot(fig, f"15. Average Score by {col_sector_1}")

# 16. Distribution of Returns by Sector (Box Plot)
if col_return_1y in df.columns and col_sector_1 in df.columns:
    data_to_plot = df[[col_return_1y, col_sector_1]].dropna(subset=[col_return_1y, col_sector_1])
    if not data_to_plot.empty and data_to_plot[col_sector_1].nunique() > 0:
        fig, ax = plt.subplots(figsize=(14, 8))
        order = data_to_plot.groupby(col_sector_1)[col_return_1y].median().sort_values(ascending=False).index
        sns.boxplot(x=col_sector_1, y=col_return_1y, data=data_to_plot, ax=ax, 
                    palette="pastel", order=order, hue=col_sector_1, legend=False)
        ax.set_xlabel(f"Sector ({col_sector_1})")
        ax.set_ylabel("1-Year Return (%)")
        plt.xticks(rotation=45, ha="right")
        save_and_close_plot(fig, f"16. Distribution of Returns by {col_sector_1} (Box Plot)")


# 17. Average Returns by Risk Country
if col_return_1y in df.columns and col_risk_country in df.columns:
    country_avg_returns = df.groupby(col_risk_country)[col_return_1y].mean().dropna().sort_values(ascending=False)
    if not country_avg_returns.empty:
        fig, ax = plt.subplots(figsize=(12, 7))
        country_avg_returns.plot(kind='bar', ax=ax, color=sns.color_palette("Spectral", len(country_avg_returns)))
        ax.set_xlabel("Risk Country")
        ax.set_ylabel("Average 1-Year Return (%)")
        plt.xticks(rotation=45, ha="right")
        save_and_close_plot(fig, "17. Average Returns by Risk Country")

# 18. Distribution of Returns by Risk Country (Box Plot)
if col_return_1y in df.columns and col_risk_country in df.columns:
    country_return_distribution_data = df[[col_return_1y, col_risk_country]].dropna(subset=[col_return_1y, col_risk_country])
    if not country_return_distribution_data.empty and country_return_distribution_data[col_risk_country].nunique() > 0:
        fig, ax = plt.subplots(figsize=(14, 8))
        # Order countries by median return for better readability
        order = country_return_distribution_data.groupby(col_risk_country)[col_return_1y].median().sort_values(ascending=False).index
        sns.boxplot(x=col_risk_country, y=col_return_1y, data=country_return_distribution_data, ax=ax, 
                    palette="coolwarm_r", order=order, hue=col_risk_country, legend=False)
        ax.set_xlabel("Risk Country")
        ax.set_ylabel("1-Year Return (%)")
        plt.xticks(rotation=45, ha="right")
        save_and_close_plot(fig, "18. Distribution of Returns by Risk Country (Box Plot)")


# 19. Average Upside by Risk Country
if col_upside in df.columns and col_risk_country in df.columns:
    country_avg_upside = df.groupby(col_risk_country)[col_upside].mean().dropna().sort_values(ascending=False)
    if not country_avg_upside.empty:
        fig, ax = plt.subplots(figsize=(12, 7))
        country_avg_upside.plot(kind='bar', ax=ax, color=sns.color_palette("viridis_r", len(country_avg_upside)))
        ax.set_xlabel("Risk Country")
        ax.set_ylabel("Average Upside Potential (%)")
        plt.xticks(rotation=45, ha="right")
        save_and_close_plot(fig, "19. Average Upside by Risk Country")
# 20. Top 20 Equities by Sharpe Ratio
if col_return_1y in df.columns and col_vol_360d in df.columns and col_equity in df.columns:
    # Define Risk-Free Rate (e.g., 1.0 for 1% if returns/volatility are in percentage points like 10.5)
    # Adjust this value as needed.
    risk_free_rate = 3.0
    
    # Create a temporary column for volatility used in Sharpe calculation to handle zeros
    df['Sharpe Volatility for Calc'] = df[col_vol_360d].replace(0, np.nan)
    
    # Calculate Sharpe Ratio
    df['Sharpe Ratio'] = (df[col_return_1y] - risk_free_rate) / df['Sharpe Volatility for Calc']
    
    # Replace infinite values (if any somehow occurred) with NaN
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    
    # Prepare data for the bar chart
    data_to_plot_sharpe = df[[col_equity, 'Sharpe Ratio']].dropna(subset=['Sharpe Ratio']).sort_values(by='Sharpe Ratio', ascending=False).head(20)
    
    if not data_to_plot_sharpe.empty:
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.barplot(x='Sharpe Ratio', y=col_equity, data=data_to_plot_sharpe, ax=ax, 
                    palette="RdYlGn", hue=col_equity, legend=False) # Using a diverging palette
        ax.set_xlabel(f"Sharpe Ratio (Rf={risk_free_rate}%)")
        ax.set_ylabel(col_equity)
        save_and_close_plot(fig, f"20. Top 20 Equities by Sharpe Ratio (Rf={risk_free_rate}%)")
    else:
        print(f"Chart 20 (Top 20 by Sharpe Ratio) skipped: No valid data after Sharpe Ratio calculation and NaN removal.")
    
    # Clean up temporary columns from df if you added them directly
    if 'Sharpe Volatility for Calc' in df.columns:
        df.drop(columns=['Sharpe Volatility for Calc'], inplace=True)
    if 'Sharpe Ratio' in df.columns: # Keep 'Sharpe Ratio' if you might use it later, or drop it
        pass # df.drop(columns=['Sharpe Ratio'], inplace=True) 

else:
    print(f"Chart 20 (Top 20 by Sharpe Ratio) skipped: Required columns '{col_return_1y}', '{col_vol_360d}', or '{col_equity}' not found.")


print(f"\nDone! All charts have been saved to the '{output_dir}' directory.")