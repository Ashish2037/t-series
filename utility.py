import pandas as pd 
from datetime import date
import joblib


def split_parameters(df, material=None, color="gold", price=0):
    bin_edges = [0, 500, 1000, 1500, 2000, 3000]
    bin_labels = ['low', 'medium', 'high', 'premium', 'luxury']
    
    # Assign prices to bins
    df["price_labels"] = pd.cut(df["price"], bins=bin_edges, labels=bin_labels, right=False)
    
    # Ensure the price is a numeric value
    if not isinstance(price, (int, float)):
        raise ValueError("Price must be a numeric value.")
    
    # Determine the price label based on the numeric price value
    price_label = pd.cut([price], bins=bin_edges, labels=bin_labels, right=False)[0]
    
    if material is None:
        df_req = df[["Date", "quantity", "color", "price_labels"]].set_index("Date")
    else:
        df_req = df[(df["base_material"] == material)][["Date", "quantity", "color", "price_labels"]].set_index("Date")
    
    df_req_color = df_req[df_req["color"] == color]
    df_req_color_price = df_req_color[df_req_color["price_labels"] == price_label]
    
    return df_req_color_price['quantity'].sum() / df_req['quantity'].sum()




def offline_split_parameters(df, material=None, color="gold", price=0):
    # Define bin edges and labels
    bin_edges = [0, 500, 1000, 1500, 2000, 3000]
    bin_labels = ['low', 'medium', 'high', 'premium', 'luxury']

    # Assign prices to bins
    df["price_labels"] = pd.cut(df["price"], bins=bin_edges, labels=bin_labels, right=False)

    # Ensure price is a numeric value
    if not isinstance(price, (int, float)):
        raise ValueError("Price must be a numeric value.")
    
    # Determine the price label based on the numeric price value
    price_label = pd.cut([price], bins=bin_edges, labels=bin_labels, right=False)[0]
    
    # Filter by material
    if material is None:
        df_req = df[["date", "quantity", "color", "price_labels", "site"]].set_index("date")
    else:
        df_req = df[df["base_material"] == material][["date", "quantity", "color", "price_labels", "site"]].set_index("date")

    # Filter by color
    df_req_color = df_req[df_req["color"] == color]

    # Filter by price label
    df_req_color_price = df_req_color[df_req_color["price_labels"] == price_label]

    # Calculate total quantities for proportion
    total_quantity = df_req["quantity"].sum()

    # Calculate proportions for each site
    site_proportions = {}
    for site in df_req_color_price["site"].unique():
        site_quantity = df_req_color_price[df_req_color_price["site"] == site]["quantity"].sum()
        site_proportions[site] = site_quantity / total_quantity if total_quantity > 0 else 0

    return 0 if not site_proportions else site_proportions

def data_genrator(days = 1,duration="week"):
    current_date = date.today()
    forecast_dates = pd.date_range(start=current_date , periods= days ,freq="D")
    if duration == "week" : 
        return forecast_dates.to_series().resample("W").asfreq().index 
    else :
        return forecast_dates.to_series().resample("ME").asfreq().index
    


def calculate_site_proportions(df):
    # Calculate the total quantity
    total_quantity = df["quantity"].sum()

    # Calculate proportions for each site
    site_proportions = {}
    for site in df["site"].unique():
        site_quantity = df[df["site"] == site]["quantity"].sum()
        site_proportions[site] = site_quantity / total_quantity if total_quantity > 0 else 0

    return site_proportions

        

def product(df,product_id):
    filter_df = df[df['product_id']==product_id]
    ratio = filter_df['quantity'].sum()/df['quantity'].sum()
    return ratio

