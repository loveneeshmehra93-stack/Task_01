import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
 
def run_analysis():
    csv_file = "store_performance.csv"
    if not os.path.exists(csv_file):
        print("error: file not found, run generate_data.py first")
        return
 
    df = pd.read_csv(csv_file)
 
    print("dataset info")
    print("number of stores:", len(df))
    print("first few rows:")
    print(df.head())
 
    print("some stats below")
 

    avg_revenue = df["Monthly_Revenue_K_USD"].mean()
    avg_ad_spend = df["Advertising_Spend_K_USD"].mean()
    avg_customers = df["Customer_Count"].mean()
    avg_rating = df["Avg_Customer_Rating"].mean()
    avg_transaction = df["Avg_Transaction_Value_USD"].mean()
 
    print("avg revenue:", round(avg_revenue, 2))
    print("avg ad spend:", round(avg_ad_spend, 2))
    print("avg customers:", round(avg_customers, 1))
    print("avg transaction value:", round(avg_transaction, 2))
    print("avg customer rating:", round(avg_rating, 2))
 
  
    df["Monthly_Profit_K_USD"] = df["Monthly_Revenue_K_USD"] - df["Operating_Cost_K_USD"]
    df["Profit_Margin_Percent"] = (df["Monthly_Profit_K_USD"] / df["Monthly_Revenue_K_USD"]) * 100
 
    avg_profit = df["Monthly_Profit_K_USD"].mean()
    avg_margin = df["Profit_Margin_Percent"].mean()
 
    print("avg profit:", round(avg_profit, 2))
    print("avg margin:", round(avg_margin, 2))
 
    print("summary stats:")
    summary_stats = df.describe()
    print(summary_stats)
 
 
    location_summary = df.groupby("Location_Type").agg({
        "Store_ID": "count",
        "Monthly_Revenue_K_USD": "mean",
        "Advertising_Spend_K_USD": "mean",
        "Customer_Count": "mean",
        "Monthly_Profit_K_USD": "mean",
        "Profit_Margin_Percent": "mean"
    }).rename(columns={"Store_ID": "Store_Count"})
 
    print("performance by location:")
    print(location_summary)
 
  
    print("making bar chart...")
 
    locs = location_summary.index
    revenues = location_summary["Monthly_Revenue_K_USD"]
    profits = location_summary["Monthly_Profit_K_USD"]
 
    x = np.arange(len(locs))
    width = 0.35
 
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(x - width/2, revenues, width, label='Avg Revenue ($K)', color='teal')
    ax.bar(x + width/2, profits, width, label='Avg Profit ($K)', color='orange')
 
    ax.set_ylabel('USD (in Thousands)')
    ax.set_title('Average Performance Metrics by Location Type')
    ax.set_xticks(x)
    ax.set_xticklabels(locs)
    ax.legend()
    ax.grid(axis='y', linestyle='--')
 
    plt.tight_layout()
    plt.savefig('bar_chart.png')
    plt.close()
 
  
    print("making scatter plot...")
 
    fig, ax = plt.subplots(figsize=(9, 6))
 
    colors_map = {"Urban": "blue", "Suburban": "purple", "Rural": "red"}
 
    for loc_type, color in colors_map.items():
        sub_df = df[df["Location_Type"] == loc_type]
        ax.scatter(sub_df["Advertising_Spend_K_USD"],
                   sub_df["Monthly_Revenue_K_USD"],
                   label=loc_type,
                   color=color,
                   alpha=0.6)
 
    ax.set_xlabel('Advertising Spend ($K)')
    ax.set_ylabel('Monthly Revenue ($K)')
    ax.set_title('Monthly Revenue vs. Advertising Budget')
    ax.legend()
    ax.grid(True, linestyle='--', alpha=0.5)
 
    plt.tight_layout()
    plt.savefig('scatter_plot.png')
    plt.close()
 

    print("making heatmap...")
 
    numeric_cols = [
        "Advertising_Spend_K_USD",
        "Customer_Count",
        "Avg_Transaction_Value_USD",
        "Monthly_Revenue_K_USD",
        "Operating_Cost_K_USD",
        "Avg_Customer_Rating",
        "Monthly_Profit_K_USD"
    ]
 
    corr_matrix = df[numeric_cols].corr()
 
    fig, ax = plt.subplots(figsize=(8, 7))
    cax = ax.imshow(corr_matrix, cmap='coolwarm', vmin=-1, vmax=1)
    fig.colorbar(cax)
 
    labels_clean = [col.replace('_', ' ').replace('K USD', '($K)').replace('USD', '($)') for col in numeric_cols]
    ax.set_xticks(np.arange(len(numeric_cols)))
    ax.set_yticks(np.arange(len(numeric_cols)))
    ax.set_xticklabels(labels_clean, fontsize=8, rotation=45, ha='right')
    ax.set_yticklabels(labels_clean, fontsize=8)
 
    ax.set_title('Correlation Matrix of Store Variables')
 
    plt.tight_layout()
    plt.savefig('correlation_heatmap.png')
    plt.close()
 
    print("all charts saved!")
 
 
if __name__ == "__main__":
    run_analysis()