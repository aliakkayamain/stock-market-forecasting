import requests
import pandas as pd
from datetime import datetime, timedelta

def fetch_stock_data(symbol, api_key):
    # Tarihleri ayarla (son 30 günlük veri)
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=99)  # Son 1 ay

    # Polygon.io Aggregates API endpoint
    url = f"https://api.polygon.io/v2/aggs/ticker/{symbol}/range/1/day/{start_date}/{end_date}?apiKey={api_key}"

    # Veriyi çek
    response = requests.get(url)
    data = response.json()

    # Eğer sonuçlarda veri yoksa hata ver
    if 'results' not in data or len(data['results']) == 0:
        raise ValueError("Polygon.io'dan yeterli veri çekilemedi. API yanıtı boş.")
    
    # Veri DataFrame'e dönüştürülüyor
    df = pd.DataFrame(data['results'])
    df['t'] = pd.to_datetime(df['t'], unit='ms')  # Zamanı datetime formatına çevir
    df.set_index('t', inplace=True)

    # İlgili sütunları al (açılış, kapanış, en yüksek, en düşük, hacim, VWAP)
    df = df[['o', 'c', 'h', 'l', 'v', 'vw']]  # Açılış, kapanış, en yüksek, en düşük, hacim, vwap

    df.columns = ['open', 'close', 'high', 'low', 'volume', 'vwap']  # Sütun adlarını düzenle

    return df