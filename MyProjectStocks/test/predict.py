import numpy as np
import pickle
from tensorflow.keras.models import load_model

def predict_last_week(model_path, scaler_path, df, symbol):
    # Modeli ve scaler'ı yükle
    model = load_model(model_path)
    with open(scaler_path, 'rb') as f:
        scaler = pickle.load(f)

    feature_columns = ['open', 'close', 'high', 'low', 'volume', 'vwap']

    # Son 5 günü iloc ile al
    df_train = df.iloc[:-5][feature_columns].values  # Eğitim verisi
    df_real = df.iloc[-5:]   # Gerçek veriler
    
    print(f"{symbol} son 5 elemanı hariç tüm elemanlar:", df_train[:-5])
    scaled_data = scaler.transform(df_train)
    print(f"{symbol} ölçeklendiirlmiş veri ( son 5 ):", scaled_data[-5:])

    # Sequence length ayarla (örneğin 8)
    sequence_length = 8  # Daha önce belirlediğimiz lookback
    if len(scaled_data) < sequence_length:
        raise ValueError(f"Veri yetersiz: Tahmin yapmak için en az {sequence_length} gün veriye ihtiyaç var.")

    # LSTM girişi olarak kullanılacak test verisini hazırla
    x_test = []
    for i in range(sequence_length, len(scaled_data)):
        x_test.append(scaled_data[i-sequence_length:i])

    x_test = np.array(x_test)

    # Tahmin yap (model sadece kapanış fiyatını tahmin edecek)
    predicted_scaled = model.predict(x_test)

    # Tahmin edilen son 5 günün sadece kapanış fiyatlarını al
    predicted_last_week_scaled = predicted_scaled[-5:]  # (5, 1) boyutunda olacak

    # Kapanış fiyatını ters ölçeklendirme (sadece kapanış fiyatını ters ölçeklendirmek)
    predicted_last_week = scaler.inverse_transform(
        np.concatenate([np.zeros((5, 5)), predicted_last_week_scaled], axis=1)
    )[:, -1]  # Sadece kapanış fiyatını ters çevir

    print(f"{symbol} için ters ölçeklendirilmiş tahmin edilen kapanış fiyatları: {predicted_last_week}")
    
    return predicted_last_week, df_real