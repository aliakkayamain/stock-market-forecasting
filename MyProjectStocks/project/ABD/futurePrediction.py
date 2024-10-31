import os
import requests
import pandas as pd
import numpy as np
from keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
import json

def predict_future_stock(symbol, model_path, start_date="2019-08-22", end_date="2024-08-26", lookback=8, future_days=5, api_key="Jpdzf05nPJhqVB5qpNZx2VbmhwVF1spP"):
    url = f'https://api.polygon.io/v2/aggs/ticker/{symbol}/range/1/day/{start_date}/{end_date}?adjusted=true&sort=asc&limit=50000&apiKey={api_key}'
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200 and 'results' in data:
        df = pd.DataFrame(data['results'])
        df['Date'] = pd.to_datetime(df['t'], unit='ms')
        df = df[['Date', 'o', 'h', 'l', 'c', 'v', 'vw']]
        df.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'VWAP']
    else:
        print(f"Veri çekilemedi: {data}")
        return None

    df = df.sort_values('Date')

    model = load_model(model_path)

    data_close = df[['Close']].values
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaler.fit(data_close)
    scaled_data = scaler.transform(data_close)

    past_days_scaled = scaled_data[-lookback:]

    predictions = []
    for _ in range(future_days):
        X_test = past_days_scaled[-lookback:]
        X_test = np.reshape(X_test, (1, X_test.shape[0], 1))
        
        predicted_price = model.predict(X_test)
        predicted_price_rescaled = scaler.inverse_transform(predicted_price)
        predictions.append(predicted_price_rescaled[0][0])

        new_scaled_value = scaler.transform(predicted_price)
        past_days_scaled = np.append(past_days_scaled, new_scaled_value)[1:]
        past_days_scaled = past_days_scaled.reshape(-1, 1)

    return predictions

def predict_all_stocks(model_dir, output_json_path, start_date="2019-08-22", end_date="2024-08-26", lookback=8, future_days=5):
    results = {}
    for model_file in os.listdir(model_dir):
        if model_file.endswith("_model.h5"):
            symbol = model_file.replace("_model.h5", "")
            model_path = os.path.join(model_dir, model_file)
            print(f"Processing {symbol}...")
            predictions = predict_future_stock(symbol, model_path, start_date, end_date, lookback, future_days)
            if predictions:
                symbol_predictions = []
                latest_closing_value = predictions[0]
                for predicted_value in predictions:
                    alsat = "al" if predicted_value > latest_closing_value else "sat"
                    symbol_predictions.append({
                        "tahmin": float(predicted_value),
                        "alsat": alsat
                    })
                results[symbol] = symbol_predictions
    
    with open(output_json_path, 'w') as json_file:
        json.dump(results, json_file, indent=4)

    print(f"Tüm tahminler {output_json_path} dosyasına kaydedildi.")


model_dir = "/Users/tbai/Documents/Vsanaliz/analiz/project/ABD/trained_models_SP500"
output_json_path = "sp500_predictions.json"


predict_all_stocks(model_dir, output_json_path)

print("Tüm hisse senetleri için tahminler tamamlandı ve JSON dosyasına kaydedildi.")