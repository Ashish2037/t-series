import joblib
import numpy as np
import pandas as pd
from datetime import date
from darts.models import NBEATSModel
from darts import TimeSeries
from darts.dataprocessing.transformers import Scaler
from utility import offline_split_parameters
from utility import calculate_proportion

def offline_earring(material,color, price, weeks,df):
    try : 
        nbeat_model_loaded = NBEATSModel.load("model/dart/nbeat_model_earring.darts")
        prophet_model = joblib.load("model/prophet_model_earring.pkl")
        print("Both models have been loaded successfully.")
        df['date'] = pd.to_datetime(df['date'])
        df.set_index("date", inplace=True)
        df1 = df.resample('W').sum().reset_index()
        series_data = TimeSeries.from_dataframe(df1, 'date', 'quantity')
        scaler = Scaler()
        scaler.fit_transform(series_data)
        y=pd.date_range(start='29-09-2024', end= weeks[-1],freq='W') 
        Y=len(y)
        print(Y)
        forecast_horizon = 18 + Y 
        forecast_nbeat = nbeat_model_loaded.predict(forecast_horizon)
        forecast_unscaled = scaler.inverse_transform(forecast_nbeat)
        forecast_unscaled_df = forecast_unscaled.pd_dataframe().reset_index()
        future = prophet_model.make_future_dataframe(periods=forecast_horizon, freq='W', include_history=False)
        forecast_prohet = prophet_model.predict(future)
        forecast_prohet = forecast_prohet[['ds', 'yhat']]
        forecast_prohet_df = pd.DataFrame(forecast_prohet)
        forecast_unscaled_df = forecast_unscaled.pd_dataframe() 
        forecast_unscaled_df.reset_index(inplace=True)
        merge_forcast = forecast_unscaled_df.merge(forecast_prohet_df, left_on="date", right_on="ds", how="inner")
        merge_forcast = merge_forcast[["date", "yhat", "quantity"]]
        merge_forcast["mean"] = merge_forcast[["yhat", "quantity"]].mean(axis=1)
        merge_forcast = merge_forcast[["date", "mean"]]
        merge_forcast.set_index("date", inplace=True)
        merge_forcast=merge_forcast[merge_forcast.index>=weeks[0] ] 
        print(merge_forcast)
        ratio = offline_split_parameters(df.reset_index(),material,color,price)
        if ratio == 0:
            return {}
        
        site_forecasts = {}
        
        for site, proportion in ratio.items():
            site_forecast = merge_forcast["mean"] * proportion
            site_forecasts[f"{site}".lower()] = round(site_forecast.sum())

        return site_forecasts
        
    except Exception as e:
        print("Error occured in  offline earring forecast " , e)
        return {}


def charm_offline(material, color, price, weeks, df):
    try:
        loaded_model = joblib.load("model/charm_forecast.pkl")

        future_dates = pd.DataFrame({"ds": weeks})
        forecast = loaded_model.predict(future_dates)["yhat"]
        ratio = offline_split_parameters(df,material,color,price)
        if ratio == 0:
            return {}
        
        site_forecasts = {}
        
        for site, proportion in ratio.items():
            site_forecast = forecast* proportion
            site_forecasts[f"{site}".lower()] = round(site_forecast.sum())

        return site_forecasts


    except Exception as e:
        print("Error occurred in offline charm forecast:", e)
        return {}
def offline_ring(material,color,price,weeks,df):
    try:
        nbeat_model_loaded = NBEATSModel.load("model/dart/nbeat_model_ring.darts")
        prophet_model = joblib.load("model/prophet_model_ring.pkl")
        print("Both models have been loaded successfully.")
        df['date'] = pd.to_datetime(df['date'])
        df.set_index("date", inplace=True)
        df1 = df.resample('W').sum().reset_index()
        series_data = TimeSeries.from_dataframe(df1, 'date', 'quantity')
        scaler = Scaler()
        scaler.fit_transform(series_data)
        y=pd.date_range(start='29-09-2024', end= weeks[-1],freq='W') 
        Y=len(y)
        print(Y)
        forecast_horizon = 18 + Y 
        forecast_nbeat = nbeat_model_loaded.predict(forecast_horizon)
        forecast_unscaled = scaler.inverse_transform(forecast_nbeat)
        forecast_unscaled_df = forecast_unscaled.pd_dataframe().reset_index()
        future = prophet_model.make_future_dataframe(periods=forecast_horizon, freq='W', include_history=False)
        forecast_prohet = prophet_model.predict(future)
        forecast_prohet = forecast_prohet[['ds', 'yhat']]
        forecast_prohet_df = pd.DataFrame(forecast_prohet)
        forecast_unscaled_df = forecast_unscaled.pd_dataframe() 
        forecast_unscaled_df.reset_index(inplace=True)
        merge_forcast = forecast_unscaled_df.merge(forecast_prohet_df, left_on="date", right_on="ds", how="inner")
        merge_forcast = merge_forcast[["date", "yhat", "quantity"]]
        merge_forcast["mean"] = merge_forcast[["yhat", "quantity"]].mean(axis=1)
        merge_forcast = merge_forcast[["date", "mean"]]
        merge_forcast.set_index("date", inplace=True)
        merge_forcast=merge_forcast[merge_forcast.index>=weeks[0] ] 
        print(merge_forcast)
        ratio = offline_split_parameters(df.reset_index(),material,color,price)
        if ratio == 0:
            return {}
        
        site_forecasts = {}
        
        for site, proportion in ratio.items():
            site_forecast = merge_forcast["mean"] * proportion
            site_forecasts[f"{site}".lower()] = round(site_forecast.sum())

        print(site_forecast)

        return site_forecasts

    except Exception as e:
        print("Error occurred in  offline ring forecast:", e)
        return {}


def offline_necklace(material,color,price,weeks,df):
    try:
        nbeat_model_loaded = NBEATSModel.load("model/dart/nbeat_model_necklace.darts")
        prophet_model = joblib.load('model/prophet_model_necklace.pkl')

        print("Both models have been loaded successfully.")
        df['date'] = pd.to_datetime(df['date'])
        df.set_index("date", inplace=True)
        df1 = df.resample('W').sum().reset_index()
        series_data = TimeSeries.from_dataframe(df1, 'date', 'quantity')
        scaler = Scaler()
        scaler.fit_transform(series_data)
        y=pd.date_range(start='29-09-2024', end= weeks[-1],freq='W') 
        Y=len(y)
        print(Y)
        forecast_horizon = 18 + Y 
        forecast_nbeat = nbeat_model_loaded.predict(forecast_horizon)
        forecast_unscaled = scaler.inverse_transform(forecast_nbeat)
        forecast_unscaled_df = forecast_unscaled.pd_dataframe().reset_index()
        future = prophet_model.make_future_dataframe(periods=forecast_horizon, freq='W', include_history=False)
        forecast_prohet = prophet_model.predict(future)
        forecast_prohet = forecast_prohet[['ds', 'yhat']]
        forecast_prohet_df = pd.DataFrame(forecast_prohet)
        forecast_unscaled_df = forecast_unscaled.pd_dataframe() 
        forecast_unscaled_df.reset_index(inplace=True)
        merge_forcast = forecast_unscaled_df.merge(forecast_prohet_df, left_on="date", right_on="ds", how="inner")
        merge_forcast = merge_forcast[["date", "yhat", "quantity"]]
        merge_forcast["mean"] = merge_forcast[["yhat", "quantity"]].mean(axis=1)
        merge_forcast = merge_forcast[["date", "mean"]]
        merge_forcast.set_index("date", inplace=True)
        merge_forcast=merge_forcast[merge_forcast.index>=weeks[0] ] 
        print(merge_forcast)
        ratio = offline_split_parameters(df.reset_index(),material,color,price)
        if ratio == 0:
            return {}
        
        site_forecasts = {}
        
        for site, proportion in ratio.items():
            site_forecast = merge_forcast["mean"] * proportion
            site_forecasts[f"{site}".lower()] = round(site_forecast.sum())

        
        return site_forecasts
    
    except Exception as e:
        print("Error occurred in offline necklace forecast:", e)
        return {}

def offline_bracelet(material,color,price,weeks,df):
    try:
        nbeat_model_loaded = NBEATSModel.load("model/dart/nbeat_model_bracelets.darts")
        prophet_model = joblib.load("model/prophet_model_bracelet.pkl") 
        print("Both models have been loaded successfully.")
        df['date'] = pd.to_datetime(df['date'])
        df.set_index("date", inplace=True)
        df1 = df.resample('W').sum().reset_index()
        series_data = TimeSeries.from_dataframe(df1, 'date', 'quantity')
        scaler = Scaler()
        scaler.fit_transform(series_data)
        
        y=pd.date_range(start='29-09-2024', end= weeks[-1],freq='W') 
        Y=len(y)
        print(Y)
        forecast_horizon = 18 + Y 
        forecast_nbeat = nbeat_model_loaded.predict(forecast_horizon)
        forecast_unscaled = scaler.inverse_transform(forecast_nbeat)
        forecast_unscaled_df = forecast_unscaled.pd_dataframe().reset_index()
        future = prophet_model.make_future_dataframe(periods=forecast_horizon, freq='W', include_history=False)
        forecast_prohet = prophet_model.predict(future)
        forecast_prohet = forecast_prohet[['ds', 'yhat']]
        forecast_prohet_df = pd.DataFrame(forecast_prohet)
        forecast_unscaled_df = forecast_unscaled.pd_dataframe() 
        forecast_unscaled_df.reset_index(inplace=True)
        merge_forcast = forecast_unscaled_df.merge(forecast_prohet_df, left_on="date", right_on="ds", how="inner")
        merge_forcast = merge_forcast[["date", "yhat", "quantity"]]
        merge_forcast["mean"] = merge_forcast[["yhat", "quantity"]].mean(axis=1)
        merge_forcast = merge_forcast[["date", "mean"]]
        merge_forcast.set_index("date", inplace=True)
        merge_forcast=merge_forcast[merge_forcast.index>=weeks[0] ] 
        print(merge_forcast)
        
        ratio = offline_split_parameters(df.reset_index(),material,color,price)
        
        if ratio == 0:
            return {}

        site_forecasts = {}
        
        for site, proportion in ratio.items():
            print("site" , "proportion",site,proportion)
            site_forecast = merge_forcast["mean"] * proportion
            site_forecasts[f"{site}".lower()] = round(site_forecast.sum())

        return site_forecasts
    
    
    except Exception as e:
        print("Error occurred in offline bracelet forecast:", e)
        return {}

def product_sale_offline(weeks,df,location,product_id):
    try:
        print("weeks",weeks)
        nbeat_model_loaded = NBEATSModel.load("model/dart/nbeat_model_offline.darts")
        prophet_model = joblib.load("model/prophet_model_offline.pkl") 
        print("Both models have been loaded successfully.")
        df['date'] = pd.to_datetime(df['date'])
        req_len = df["product_id"].nunique()
        df.set_index("date", inplace=True)
        df1 = df.resample('W').sum().reset_index()
        series_data = TimeSeries.from_dataframe(df1, 'date', 'quantity')
        scaler = Scaler()
        scaler.fit_transform(series_data)
        y=pd.date_range(start='29-09-2024', end= weeks[-1],freq='W') 
        Y=len(y)
        print(Y)
        forecast_horizon = 18+ Y 
        forecast_nbeat = nbeat_model_loaded.predict(forecast_horizon)
        forecast_unscaled = scaler.inverse_transform(forecast_nbeat)
        forecast_unscaled_df = forecast_unscaled.pd_dataframe().reset_index()
        future = prophet_model.make_future_dataframe(periods=forecast_horizon, freq='W', include_history=False)
        forecast_prohet = prophet_model.predict(future)
        forecast_prohet = forecast_prohet[['ds', 'yhat']]
        forecast_prohet_df = pd.DataFrame(forecast_prohet)
        forecast_unscaled_df = forecast_unscaled.pd_dataframe() 
        forecast_unscaled_df.reset_index(inplace=True)
        merge_forcast = forecast_unscaled_df.merge(forecast_prohet_df, left_on="date", right_on="ds", how="inner")
        merge_forcast = merge_forcast[["date", "yhat", "quantity"]]
        merge_forcast["mean"] = merge_forcast[["yhat", "quantity"]].mean(axis=1)
        merge_forcast = merge_forcast[["date", "mean"]]
        merge_forcast.set_index("date", inplace=True)
        #merge_forcast=merge_forcast[(merge_forcast.index>=weeks[0]) & (merge_forcast.index <= weeks[-1]) ]
        merge_forcast=merge_forcast[merge_forcast.index >= weeks[0]]  
        print("mf",merge_forcast)
        
        ratio = calculate_proportion(df.reset_index(),product_id)
        if ratio == 0:
            return {} 
        site_forecasts = {}
        
        for site, proportion in ratio.items():
            site_forecast = merge_forcast["mean"] * proportion
            site_forecasts[f"{site}".lower()] = round(site_forecast.sum())

        print("site forcast",site_forecasts)
        
        return site_forecasts[location]
    
    except Exception as e:
        print("Error occurred in offline high forecast:", e)
        return {}
