import requests
import pandas as pd
from datetime import datetime, timedelta

# Polygon.io API verilerini çek
def fetch_stock_data(symbol, api_key, start_date, end_date):
    """
    Belirtilen tarih aralığında borsa verilerini çeker.
    
    :param symbol: Hisse senedi sembolü
    :param api_key: Polygon.io API anahtarı
    :param start_date: Başlangıç tarihi (YYYY-MM-DD)
    :param end_date: Bitiş tarihi (YYYY-MM-DD)
    """
    print(f"{symbol} için veri çekiliyor...")
    print(f"Başlangıç tarihi: {start_date}")
    print(f"Bitiş tarihi: {end_date}")
    
    # Polygon.io Aggregates API endpoint
    url = f"https://api.polygon.io/v2/aggs/ticker/{symbol}/range/1/day/{start_date}/{end_date}?apiKey={api_key}"
    
    response = requests.get(url)
    data = response.json()

    # API yanıtını kontrol et
    if 'results' not in data or len(data['results']) == 0:
        raise ValueError(f"{symbol} için veri bulunamadı.")
    
    # Veriyi DataFrame'e çevir
    df = pd.DataFrame(data['results'])
    df['t'] = pd.to_datetime(df['t'], unit='ms')  # Zaman damgasını datetime formatına çevir
    df.set_index('t', inplace=True)
    
    # Giriş özelliklerini belirle (açılış, kapanış, en yüksek, en düşük, hacim, hacim ağırlıklı ortalama)
    feature_columns = ['o', 'c', 'h', 'l', 'v', 'vw']
    available_columns = df.columns
    
    # Sadece mevcut sütunları kullan
    df = df[[col for col in feature_columns if col in available_columns]]

    return df  # Veriyi bellekte tut