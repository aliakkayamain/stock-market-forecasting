import requests
import pandas as pd
import matplotlib.pyplot as plt
import os
from sklearn.preprocessing import MinMaxScaler
import numpy as np
from keras.models import Sequential
from keras.layers import GRU, Dense, Dropout
from keras.callbacks import EarlyStopping
import tensorflow as tf
import time  # Eklenen kütüphane
import gc

api_key = "Jpdzf05nPJhqVB5qpNZx2VbmhwVF1spP"
end_date = "2024-01-01"
start_date = "2014-09-17"
symbol_csv_path = '/Users/tbai/Documents/Vsanaliz/analiz/project/ABD/Data/sp500_symbols.csv'
save_dir = "/Users/tbai/Documents/Vsanaliz/analiz/project/ABD/GRU_1"


if not os.path.exists(save_dir):
    os.makedirs(save_dir)


symbols_df = pd.read_csv(symbol_csv_path)
symbols = symbols_df['Symbol'].tolist()


def fetch_and_process_data(symbol):
    print(f"Veri çekiliyor: {symbol}")
    url = f'https://api.polygon.io/v2/aggs/ticker/{symbol}/range/1/day/{start_date}/{end_date}?adjusted=true&sort=asc&limit=50000&apiKey={api_key}'
    
    try:
        response = requests.get(url)
        response.raise_for_status() 

        data = response.json()

        if 'results' in data:
            df = pd.DataFrame(data['results'])
            df['date'] = pd.to_datetime(df['t'], unit='ms')
            df = df[['date', 'o', 'h', 'l', 'c', 'v', 'vw']]
            df.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'VWAP']
            return df
        else:
            print(f"Veri bulunamadı: {symbol}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"API hatası: {e}")
        return None


def normalize_data(df):
    min_max_scaler = MinMaxScaler()
    df['Close'] = min_max_scaler.fit_transform(df['Close'].values.reshape(-1, 1))
    return df, min_max_scaler


def load_data(stock, seq_len, valid_set_size_percentage, test_set_size_percentage):
    data_raw = stock.to_numpy()  
    data = []

    for index in range(len(data_raw) - seq_len):
        data.append(data_raw[index: index + seq_len])
    
    data = np.array(data)
    
    valid_set_size = int(np.round(valid_set_size_percentage / 100 * data.shape[0]))
    test_set_size = int(np.round(test_set_size_percentage / 100 * data.shape[0]))
    train_set_size = data.shape[0] - (valid_set_size + test_set_size)
    
    x_train = data[:train_set_size, :-1, :]
    y_train = data[:train_set_size, -1, :]
    
    x_valid = data[train_set_size:train_set_size + valid_set_size, :-1, :]
    y_valid = data[train_set_size:train_set_size + valid_set_size, -1, :]
    
    x_test = data[train_set_size + valid_set_size:, :-1, :]
    y_test = data[train_set_size + valid_set_size:, -1, :]
    
    return [x_train, y_train, x_valid, y_valid, x_test, y_test]


def create_gru_model(input_shape):
    regressorGRU = Sequential()
    
    regressorGRU.add(GRU(units=50, return_sequences=True, input_shape=input_shape, activation='tanh'))
    regressorGRU.add(Dropout(0.2))
    
    regressorGRU.add(GRU(units=50, return_sequences=True, activation='tanh'))
    regressorGRU.add(Dropout(0.2))
    
    regressorGRU.add(GRU(units=50, return_sequences=True, activation='tanh'))
    regressorGRU.add(Dropout(0.2))
    
    regressorGRU.add(GRU(units=50, activation='tanh'))
    regressorGRU.add(Dropout(0.2))
    
    regressorGRU.add(Dense(units=1))
    
    optimizer = tf.keras.optimizers.Adam(learning_rate=0.0001)
    regressorGRU.compile(optimizer=optimizer, loss='mean_squared_error')

    return regressorGRU


seq_len = 20
valid_set_size_percentage = 10
test_set_size_percentage = 10
batch_size = 16
n_epochs = 150


for symbol in symbols:
    df = fetch_and_process_data(symbol)
    
    if df is not None:
        df_stock_norm, scaler = normalize_data(df[['Close']].copy()) 
        
        x_train, y_train, x_valid, y_valid, x_test, y_test = load_data(df_stock_norm, seq_len, valid_set_size_percentage, test_set_size_percentage)
        
        y_train = y_train[:, -1]
        y_valid = y_valid[:, -1]
        
        train_dataset = tf.data.Dataset.from_tensor_slices((x_train, y_train)).batch(batch_size).prefetch(tf.data.experimental.AUTOTUNE)
        valid_dataset = tf.data.Dataset.from_tensor_slices((x_valid, y_valid)).batch(batch_size).prefetch(tf.data.experimental.AUTOTUNE)
        

        model = create_gru_model((x_train.shape[1], 1))
        
        early_stopping = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True) 
        
        print(f"Eğitim başlıyor: {symbol}")
        
        history = model.fit(train_dataset, 
                            epochs=n_epochs, 
                            validation_data=valid_dataset, 
                            callbacks=[early_stopping])
        
        model_save_path = os.path.join(save_dir, f"GRU_{symbol}_model.h5")
        model.save(model_save_path)
        
        print(f"Model kaydedildi: {model_save_path}")
        

        del df, df_stock_norm, x_train, y_train, x_valid, y_valid, x_test, y_test, train_dataset, valid_dataset, model, history
        gc.collect()  # Belleği temizle
        
        time.sleep(1)  
        
        time.sleep(1)  
        
    else:
        print(f"{symbol} için veri bulunamadı.")