import numpy as np
from sklearn.preprocessing import MinMaxScaler
import os
import pickle

def preprocess_data(df, symbol, scaler_dir, lookback=8):
    # Kullanılacak sütunlar (açılış, kapanış, en yüksek, en düşük, hacim, hacim ağırlıklı ortalama)
    feature_columns = ['o', 'c', 'h', 'l', 'v', 'vw']
    data = df[feature_columns].values  # Veriyi numpy array olarak alıyoruz
    
    # Veriyi normalize et
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(data)

    # Scaler'ı kaydet
    os.makedirs(scaler_dir, exist_ok=True)
    scaler_path = os.path.join(scaler_dir, f"{symbol}_scaler.pkl")
    with open(scaler_path, 'wb') as f:
        pickle.dump(scaler, f)
    
    # Lookback penceresi için veriyi hazırlama
    x_train, y_train = [], []
    for i in range(lookback, len(scaled_data)):
        x_train.append(scaled_data[i-lookback:i])  # Tüm özellikleri kullanarak girdi oluştur
        y_train.append(scaled_data[i, 1])  # Kapanış fiyatı (c) çıkış olarak kullanılıyor

    return np.array(x_train), np.array(y_train), scaler

    