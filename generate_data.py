import pandas as pd
import numpy as np
 

np.random.seed(42)
n_stores = 50
 
store_ids = [f"ST{i:03d}" for i in range(1, n_stores + 1)]
locations = np.random.choice(["Urban", "Suburban", "Rural"], size=n_stores, p=[0.4, 0.4, 0.2])
advertising_spend = np.random.uniform(5, 50, size=n_stores)
 
location_traffic_multiplier = np.where(locations == "Urban", 1.2, np.where(locations == "Suburban", 1.0, 0.7))
customer_count = (1000 + advertising_spend * 80 + np.random.normal(0, 300, size=n_stores)) * location_traffic_multiplier

customer_count = np.clip(customer_count, 300, None).astype(int)
 
avg_transaction_value = np.random.normal(15, 3, size=n_stores)
avg_transaction_value = np.clip(avg_transaction_value, 5, 30)
 
monthly_revenue = (customer_count * avg_transaction_value / 1000.0) + np.random.normal(0, 5, size=n_stores)
monthly_revenue = np.clip(monthly_revenue, 10, None)
 
avg_rating = np.random.normal(4.0, 0.5, size=n_stores)
avg_rating = np.clip(avg_rating, 1.0, 5.0).round(1)
 
location_cost_baseline = np.where(locations == "Urban", 20, np.where(locations == "Suburban", 15, 10))
operating_cost = location_cost_baseline + (monthly_revenue * 0.45) + np.random.normal(0, 3, size=n_stores)
operating_cost = np.clip(operating_cost, 5, None)
 
df = pd.DataFrame({
    "Store_ID": store_ids,
    "Location_Type": locations,
    "Advertising_Spend_K_USD": np.round(advertising_spend, 2),
    "Customer_Count": customer_count,
    "Avg_Transaction_Value_USD": np.round(avg_transaction_value, 2),
    "Monthly_Revenue_K_USD": np.round(monthly_revenue, 2),
    "Operating_Cost_K_USD": np.round(operating_cost, 2),
    "Avg_Customer_Rating": avg_rating
})
 
csv_path = "store_performance.csv"
df.to_csv(csv_path, index=False)
print("done, file saved")
print(df.head())