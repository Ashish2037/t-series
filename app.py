from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from utility import data_genrator 
from online_forecasting_functions import ring , necklace , bracelet , earring , charm , product_sale
from offline_forecasting_functions import offline_ring , offline_necklace , offline_bracelet ,offline_earring , charm_offline , offline_high_sale , offline_medium_sale , offline_low_sale


app = Flask(__name__)

CORS(app)

@app.route('/', methods=['GET'])
def homepage():
    return jsonify({"message":"server online"})

@app.route('/forecast2', methods=['GET', 'POST'])
def forecast2():
   
    data = request.get_json()
    categorie = data.get('categorie').lower()
    material = data.get('material').lower()
    color = data.get('color').lower()
    price = data.get('price')
    days = data.get('days')
    
    
    if categorie =='bracelet':
        ## online Prediction 
        df = pd.read_csv("data/bracelet.csv")
        weeks = data_genrator(days,duration="week") 
        result = bracelet(material,color,price,weeks,df)

        ## offline Prediction
        df_offline = pd.read_csv('data/bracelet_offline.csv')
        weeks = data_genrator(days,duration="week") 
        result_offline = offline_bracelet(material,color,price,weeks,df_offline)
          

    elif categorie =='earring':
        ## online Prediction 
        df = pd.read_csv("data/earring.csv")
        result = earring(material,color,price,days,df)

        ## offline Prediction
        df_offline = pd.read_csv('data/earring_offline.csv')
        weeks = data_genrator(days,duration="week") 
        result_offline = offline_earring(material,color,price,weeks,df_offline)


    
    elif categorie =='ring':
        ## online Prediction 
        df = pd.read_csv("data/ring.csv")
        weeks = data_genrator(days,duration="week") 
        result = ring(material,color,price,weeks,df)

        ## offline Prediction
        df_offline = pd.read_csv('data/ring_offline.csv')
        weeks = data_genrator(days,duration="week") 
        result_offline = offline_ring(material,color,price,weeks,df_offline)

    elif categorie =='necklace':
        ## online Prediction 
        df = pd.read_csv("data/necklace.csv")
        weeks = data_genrator(days,duration="week") 
        result = necklace(material,color,price,weeks,df)


        ## offline Prediction
        df_offline = pd.read_csv('data/necklace_offline.csv')
        weeks = data_genrator(days,duration="week") 
        result_offline = offline_necklace(material,color,price,weeks,df_offline)
  

    elif categorie =='charm':
        ## online Prediction 
        df = pd.read_csv("data/charm_df.csv")
        weeks = data_genrator(days,duration="week") 
        result = charm(material,color,price,weeks,df)

        ## offline Prediction
        df_offline =pd.read_csv('data/charm_offline.csv')
        weeks = data_genrator(days,duration="week") 
        result_offline = charm_offline(material,color,price,weeks,df_offline)

    else:
        return jsonify({'message': "categorie does not exist"})
    
    print("offline resukt new ",result_offline)
    
    result_offline = {"offline" :  "category does not exist" } if not result_offline else result_offline
    result = "category does not exist" if result == 0 else result
    return jsonify({'online': result , **result_offline})


@app.route('/forecast1', methods=['GET', 'POST'])
def forecast1():
    print("the developer made this app is great greast")
    data = request.get_json()
    location = data.get('location').lower()
    product_id = str(data.get('product_id'))
    product_id = float(f"{product_id}.{0}")
    days = int(data.get('days'))
    weeks = data_genrator(days,duration="week") 
    result = None
    if location=='online':
        result = product_sale(weeks,product_id)
    else:
        result = product_sale_offline(weeks,product_id,location)

    return jsonify({location:result})

if __name__ == '__main__':
    app.run(debug=True)
