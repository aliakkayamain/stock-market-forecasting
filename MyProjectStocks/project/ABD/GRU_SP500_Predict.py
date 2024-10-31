import requests
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
import numpy as np
from tensorflow.keras.models import load_model
import gc 

api_key = "Jpdzf05nPJhqVB5qpNZx2VbmhwVF1spP"
end_date = "2024-09-17"
start_date = "2024-01-02"


def fetch_data(symbol, limit=100):
    try:
        print(f"Veri çekiliyor: {symbol}")
        url = f'https://api.polygon.io/v2/aggs/ticker/{symbol}/range/1/day/{start_date}/{end_date}?adjusted=true&sort=desc&limit={limit}&apiKey={api_key}'
        
        print("Veriler başarıyla çekildi....")
        response = requests.get(url)
        response.raise_for_status() 
        
        data = response.json()
        
        if 'results' in data:
            df = pd.DataFrame(data['results'])
            df['date'] = pd.to_datetime(df['t'], unit='ms')
            df = df[['date', 'o', 'h', 'l', 'c', 'v', 'vw']]
            df.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'VWAP']
            df = df.sort_values('Date') 
            return df
        else:
            print(f"Veri bulunamadı: {symbol}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"HTTP hatası: {e}")
        return None


def normalize_data(df):
    scaler = MinMaxScaler()
    df['Close'] = scaler.fit_transform(df['Close'].values.reshape(-1, 1))
    
    print("Veriler normalize edildi")
    return df, scaler


def prepare_data(stock, seq_len):
    data_raw = stock.to_numpy()
    data = []
    
    for index in range(len(data_raw) - seq_len): 
        data.append(data_raw[index: index + seq_len])
    
    data = np.array(data)
    
    x_test = data[:, :-1, :]
    y_test = data[:, -1, :]
    
    return x_test, y_test


model_path = "/Users/tbai/Documents/Vsanaliz/analiz/project/ABD/GRU_1/GRU_ACN_model.h5"
print(f"Yüklenen model.........: {model_path}")
model = load_model(model_path)



def test_model_with_real_prices(symbol, seq_len=20):
  
    df_100 = fetch_data(symbol, limit=100)  
   
    df_500 = fetch_data(symbol, limit=500)  
    
    if df_100 is not None and df_500 is not None:
        df_stock_norm, scaler = normalize_data(df_100[['Date', 'Close']].copy())  
       
        x_test, y_test = prepare_data(df_stock_norm[['Close']], seq_len)
        
        print("Test Başlıyor.....")
        y_test_pred = model.predict(x_test)
       
        y_test_real = scaler.inverse_transform(y_test.reshape(-1, 1))
        y_test_pred_real = scaler.inverse_transform(y_test_pred)
        
        test_dates = df_100['Date'][-len(y_test):] 
        
      
        df_500_filtered = df_500[df_500['Date'] < test_dates.iloc[0]]

       
        plt.figure(figsize=(12, 5))
        
       
        plt.plot(df_500_filtered['Date'], df_500_filtered['Close'], label='Geçmiş Veri', color='black')
        
        
        plt.plot(test_dates, y_test_real, label='Gerçek Veri (Test)', color='blue', linestyle='dashed')
        
      
        plt.plot(test_dates, y_test_pred_real, label='Tahmin  (Test)', color='red')
        
        plt.title(f'{symbol} İçin Gerçek vs Tahmin Edilen Fiyatlar')
        plt.xlabel('Zaman')
        plt.ylabel('Fiyat')
        plt.xticks(rotation=45)
        plt.legend()
        plt.tight_layout()
        plt.show()

        del df_100, df_500, df_stock_norm, x_test, y_test, y_test_pred
        gc.collect()
        
        return y_test_real, y_test_pred_real
    else:
        print(f"{symbol} için veri bulunamadı.")
        return None, None



test_model_with_real_prices("ACN", seq_len=20)