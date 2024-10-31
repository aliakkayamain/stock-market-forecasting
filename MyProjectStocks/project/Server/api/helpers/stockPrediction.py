import os
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import load_model
from api.helpers.getHistoricalData import get_historical_data
import pandas as pd


def load_symbols(symbols_file):
    """
    SP500 sembollerini CSV dosyasından yükler. İlk satır başlık olabilir, bu yüzden atlanıyor.
    """
    if not os.path.exists(symbols_file):
        raise FileNotFoundError(f"{symbols_file} bulunamadı.")
    
    symbols_df = pd.read_csv(symbols_file, header=None)  
    symbols = symbols_df[0].tolist()

    if symbols[0].lower() == 'symbol':
        symbols = symbols[1:]

    return symbols


def load_model_for_symbol(symbol, model_dir):
    model_filename = f"{symbol}_model.h5"
    model_path = os.path.join(model_dir, model_filename)  

    print(f"Tahmin öncesi predict_stock içindeki model yolu-------------------------------------------------------------: {model_path}") 

    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model for symbol {symbol} not found at {model_path}")

    return load_model(model_path)


def predict_future_stock(symbol, model_dir, start_date, end_date, lookback, future_days):
    """
    Sembol ve model yolunu kullanarak gelecekteki fiyatları tahmin eder.
    """
   
    close_prices = get_historical_data(symbol, start_date, end_date)

    if not close_prices or len(close_prices) == 0:
        raise ValueError(f"Could not retrieve historical data for symbol {symbol}")

    if len(close_prices) < lookback:
        lookback = len(close_prices)
        

 
    close_prices = np.array(close_prices).reshape(-1, 1)
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(close_prices)

    model = load_model_for_symbol(symbol, model_dir)

    print(f"Model path after load_model_for_symbol-------------------------------------------------------------: {model_dir}/{symbol}_model.h5")

    predictions = []

    for _ in range(future_days):
        X_test = np.array(scaled_data[-lookback:]).reshape((1, lookback, 1))
        predicted_price = model.predict(X_test)

        predicted_price_rescaled = scaler.inverse_transform(predicted_price)
        predictions.append(float(predicted_price_rescaled[0, 0]))

     
        scaled_data = np.append(scaled_data, scaler.transform(predicted_price))[-lookback:]

    return predictions