import os
import json
from datetime import datetime, timedelta
import time 
import requests # type: ignore
import glob
from config.config import Config


def load_predictions_from_file(tarih):
    """
    Verilen tarih ile başlayan tahmin dosyasını yükler. Dosya ismi formatı şu şekildedir:
    hisseler_predictions_{tarih}_saatdakika.json
    """
    folder_path = Config.predictions_directory
    

    search_pattern = f"predictions_{tarih}_*.json"
    matching_files = glob.glob(os.path.join(folder_path, search_pattern))
    
    if not matching_files:
        print(f"Tarih ile eşleşen dosya bulunamadı: {search_pattern}")
        return None
    
    # En son oluşturulan dosyayı seç bu kısımda en son kayıt edilen dosyayı alıyor
    latest_file = max(matching_files, key=os.path.getctime)
    print(f"Bulunan dosya: {latest_file}")  
    
    with open(latest_file, 'r') as file:
        data = json.load(file)
    
    return data.get("stocks", [])



POLYGON_API_KEY = Config.POLYGON_API_KEY
def get_actual_stock_value(symbol, analiz_tarihi):
    """
    Polygon.io API'sini kullanarak belirtilen hisse için bir önceki iş gününün kapanış fiyatını alır.
    """
    max_retries = 5
    wait_time = 1
    
    # 'analiz_tarihi' formatı 'YYYYMMDD' olarak geliyor, bunu 'YYYY-MM-DD' formatına çevirelim
    formatted_date = datetime.strptime(analiz_tarihi, "%Y%m%d").strftime("%Y-%m-%d")

    for retry in range(max_retries):
        url = f"https://api.polygon.io/v1/open-close/{symbol}/{formatted_date}?adjusted=true&apiKey={POLYGON_API_KEY}"
        
        try:
            response = requests.get(url)
            response.raise_for_status()  # HTTP hatalarını kontrol eder
            
            data = response.json()
            closing_price = data.get("close")
            
            if closing_price is not None:
                print(f"Kapanış fiyatı: {closing_price} - Sembol: {symbol}, Tarih: {formatted_date}")
                print(f"Sembol: {symbol} için analiz yapılıyor...")
                return closing_price, formatted_date
            else:
                print(f"Veri bulunamadı: {symbol} için {formatted_date} tarihinde kapanış değeri yok.")
                
        
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP hatası: {http_err}")
            if response.status_code == 429:  # Eğer 429 hatası aldıysak, bekle ve tekrar dene
                print(f"429 hatası alındı, {wait_time} saniye bekleniyor...")
                time.sleep(wait_time)
                wait_time *= 2  
        
        # Eğer veri bulunamazsa, bir önceki iş gününe git yani şuanın kapanış verisi yoksa en sonki kapanış verisini dikkate alır
        formatted_date = (datetime.strptime(formatted_date, "%Y-%m-%d") - timedelta(days=1)).strftime("%Y-%m-%d")

    print(f"{symbol} için son {max_retries} iş günü içerisinde kapanış değeri bulunamadı.")
    return None, None  





def analyze_predictions(predictions, analiz_tarihi):
    """
    Tahmin edilen ve belirtilen iş gününün gerçek hisse değerlerini karşılaştırır.
    """
    analysis_results = []
    

    tahmin_tarihi = (datetime.strptime(analiz_tarihi, "%Y%m%d") + timedelta(days=1)).strftime("%Y-%m-%d")
    
    for prediction in predictions:
        # 'symbol' ve 'HisseKodu' anahtarlarını kontrol et
        symbol = prediction.get('symbol') or prediction.get('HisseKodu')
        if not symbol:
            print(f"Symbol anahtarı bulunamadı: {prediction}")
            continue  
        
        # 'predict' ve 'Tahmin' anahtarlarını kontrol et
        predicted_value = prediction.get('predict') or prediction.get('Tahmin')
        if predicted_value is None:
            print(f"Predicted value anahtarı bulunamadı: {prediction}")
            continue  

        # 'forecast_date' ve 'TahminTarihi' anahtarlarını kontrol et
        gercek_deger_tarihi = prediction.get('forecast_date') or prediction.get('TahminTarihi')
        if not gercek_deger_tarihi:
            print(f"Forecast date anahtarı bulunamadı: {prediction}")
            continue  
        
      
        actual_value, actual_date = get_actual_stock_value(symbol, gercek_deger_tarihi.replace("-", ""))

        if actual_value is None:
            continue  
        
        fark = predicted_value - actual_value
        oran = (fark / actual_value) * 100 if actual_value != 0 else 0

   
        analysis_results.append({
            "symbol": symbol,
            "forecast_date": tahmin_tarihi,  # Route'tan gelen tarihin bir gün sonrası
            "real_value": float(actual_value),
            "real_value_date": gercek_deger_tarihi,  # JSON dosyasındaki 'TahminTarihi'
            "predicted_value": float(predicted_value),
            "difference": float(fark),
            "ratio": float(oran)
        })

    return analysis_results