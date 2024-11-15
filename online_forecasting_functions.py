from utility import split_parameters , data_genrator, product
import joblib 
from prophet import Prophet
import pandas as pd
import numpy as np 

# Ring Forecasting 
def ring(material,color, price, weeks,df):
    try : 
        print('ring')
        forecast=None
        if material=='brass':
            trend = joblib.load("model/ring_brass_trend.joblib")
            seasonality = joblib.load("model/ring_brass_seasonality.joblib")  
            trend_forecast = trend.predict(start = weeks[0] , end = weeks[-1])
            seasonality_forecast = seasonality.predict(start = weeks[0] , end = weeks[-1])
            final_forecast = trend_forecast + seasonality_forecast  
            ratio = split_parameters(df,material,color,price)
            forecast = final_forecast*ratio
        
        elif material=='sterling-silver':
            loaded_model = joblib.load("model/ring_silver.joblib")
            future_dates = pd.DataFrame({"ds": weeks})
            forecast = loaded_model.predict(future_dates)["yhat"]
            ratio = split_parameters(df,material,color,price)
            forecast = forecast*ratio
        
        return round(sum(forecast.tolist())) if forecast is not None else 0
    except Exception as e:
        print("Error occured in ring forecast " , e)
        return 0

# Necklace Forecasting 
def necklace(material,color,price,weeks,df):
    try:
        print('Necklace')
        forecast=None
        
        if material=='brass':
            loaded_model1 = joblib.load("model/necklace_brass_seasonality.joblib")
            loaded_model2 = joblib.load('model/necklace_brass_trend.joblib')
            forecast1 = loaded_model1.predict(start = weeks[0] , end = weeks[-1])
            forecast2 = loaded_model2.predict(start = weeks[0] , end = weeks[-1])
            final_forecast =np.expm1(forecast1*forecast2)
            final_forecast.dropna(inplace =True)       
            ratio = split_parameters(df,material,color,price)
            forecast = final_forecast*ratio   
        
        
        elif material=='sterling-silver':
            loaded_model = joblib.load("model/necklace_silver.joblib")
            data_index = pd.date_range(start="24-12-2023" , end=weeks[-1],freq = "W")
            forecast_exog = pd.DataFrame({"date":data_index})
            forecast_exog["q"] = forecast_exog["date"].dt.quarter
            forecast_exog["month"] = forecast_exog["date"].dt.month
            forecast_exog.set_index("date",inplace=True)
            forecast = np.exp(loaded_model.forecast(len(forecast_exog),exog= forecast_exog[["q","month"]]))   
            forecast = forecast[(forecast.index >= weeks[0])]
            ratio = split_parameters(df,material,color,price)
            forecast = forecast*ratio


        elif material=='stainless-steel':
            model1 = joblib.load("model/necklace_steel_seasonality.joblib")
            model2 = joblib.load('model/necklace_steel_trend.joblib')
            forecast1 = model1.predict(start = weeks[0] , end = weeks[-1])
            forecast2 = model2.predict(start = weeks[0] , end = weeks[-1])
            final_forecast =np.expm1(forecast1*forecast2)
            final_forecast.dropna(inplace =True)       
            ratio = split_parameters(df,material,color,price)
            forecast = final_forecast*ratio
        
        return round(sum(forecast.tolist())) if forecast is not None else 0
    except Exception as e:
        print("Error occured in necklace forecast " , e)
        return 0

# Bracelet forecating
def bracelet(material,color,price,weeks,df):
    try : 
        print('bracelet')
        forecast=None

        if material=='brass':
            loaded_model = joblib.load("model/bracelet_brass.pkl")
            forecast = loaded_model.predict(start = weeks[0] , end = weeks[-1])
            ratio = split_parameters(df,material,color,price)
            forecast = forecast*ratio
        
        elif material=='sterling-silver':
            loaded_model = joblib.load("model/bracelet_silver.pkl")
            forecast = loaded_model.predict(start = weeks[0] , end = weeks[-1])
            ratio = split_parameters(df,material,color,price)
            forecast = forecast*ratio 
        
        elif material=='stainless-steel':
            model1 = joblib.load("model/bracelet_steel_season.pkl")
            model2 = joblib.load("model/bracelet_steel_trend.pkl")
            forecast1 = model1.predict(start = weeks[0] , end = weeks[-1])
            forecast2 = model2.predict(start = weeks[0] , end = weeks[-1])
            final_forecast =np.expm1(forecast1*forecast2)
            final_forecast.dropna(inplace =True) 
            ratio = split_parameters(df,material,color,price)
            forecast = final_forecast*ratio

        return round(sum(forecast.tolist())) if forecast is not None else 0
    
    except Exception as e:
        print("Error occured in bracelet forecast " , e)
        return 0

# Earring Forecasting
def earring(material, color, price, days, df):
    try:
        print('earring')  
        material_to_model = {
            'brass': ("model/earring_brass.pkl", "month"),
            'sterling-silver': ("model/earring_silver.pkl", "month"),
            'stainless-steel': ("model/earring_steel.pkl", "week")
        } 
        # Check if material is valid
        if material in material_to_model:
            model_file, duration = material_to_model[material]
            intervals = data_genrator(days, duration=duration)
            loaded_model = joblib.load(model_file)
            forecast = loaded_model.predict(start=intervals[0], end=intervals[-1])
            ratio = split_parameters(df, material, color, price)
            forecast = forecast * ratio
            return round(sum(forecast.tolist()))
        # Return 0 if material is not found in the mapping
        return 0
    except Exception as e:
        print("Error occurred in earring forecast:", e)
        return 0


# Charm Forecasting  
def charm(material,color,price, weeks,df):
    try :
        print('charm')
        forecast = None
        if material=='sterling-silver':
            loaded_model = joblib.load("model/charm_model.pkl")
            forecast = loaded_model.predict(start = weeks[0] , end = weeks[-1])
            ratio = split_parameters(df,material,color,price)
            forecast = forecast*ratio
        return round(sum(forecast.tolist())) if forecast is not None else 0
    except Exception as e:
        print("Error occured in charm forecast " , e)
        return 0

def product_sale(weeks,product_id):
    try :
        forecast = None
        model = joblib.load("model/final_sales.joblib")
        forecast = model.predict(start = weeks[0] , end = weeks[-1])
        final_forecast = np.exp(forecast)
        df = pd.read_csv("data/final_data.csv")
        ratio = product(df,product_id)
        final_forecast = final_forecast
        result = sum(final_forecast.tolist())
        return round(result*ratio) if final_forecast is not None else 0
    
    except Exception as e:
        print("Error occured in high_sales forecast " , e)
        return 0
    
