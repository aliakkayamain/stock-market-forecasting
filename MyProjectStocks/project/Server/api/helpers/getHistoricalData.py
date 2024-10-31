from datetime import datetime, timedelta
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from config.config import Config

POLYGON_API_KEY = Config.POLYGON_API_KEY

def get_historical_data(symbol, start_date=None, end_date=None, days=7):
    """
    Belirtilen sembol için tarihsel verileri Polygon API'den çeker.
    Eğer `start_date` ve `end_date` belirtilmezse, son `days` kadar veriyi çeker.
    
    :param symbol: Hisse senedi sembolü
    :param start_date: Başlangıç tarihi (opsiyonel)
    :param end_date: Bitiş tarihi (opsiyonel)
    :param days: Geçmiş veri için istenen gün sayısı (default: 7)
    :return: high_prices, low_prices, close_prices listeleri
    """

  
    if not end_date:
        end_date = datetime.today().strftime("%Y-%m-%d")
    if not start_date:
        start_date = (datetime.today() - timedelta(days=days)).strftime("%Y-%m-%d")

    url = f"https://api.polygon.io/v2/aggs/ticker/{symbol}/range/1/day/{start_date}/{end_date}?adjusted=true&sort=asc&limit=120&apiKey={POLYGON_API_KEY}"
    

    retry_strategy = Retry(
        total=5,  # Maksimum 5 tekrar deneme
        backoff_factor=1,  # Her denemede bekleme süresini arttır
        status_forcelist=[429, 500, 502, 503, 504],  #bu hatalar için tekrara denemee yapıcak
        allowed_methods=["GET"] 
    )
    
    adapter = HTTPAdapter(max_retries=retry_strategy)
    http = requests.Session()
    http.mount("https://", adapter)

    try:
        response = http.get(url)
        data = response.json()

        if response.status_code == 200 and 'results' in data:
            close_prices = [day['c'] for day in data['results'] if 'c' in day] # o günün kapanış değeri
            high_prices = [day['h'] for day in data['results'] if 'h' in day] #o günün en yükske değeri
            low_prices = [day['l'] for day in data['results'] if 'l' in day] # o günün en düşük değeri
            open_prices = [day['o'] for day in data['results'] if 'o' in day] # açılış değerini de çekiyorum en son bunu ekledim
            
            available_days = len(close_prices)
            print(f"Polygon API'den {symbol} için {available_days} günün verisi alındı: {close_prices}")

            if available_days < days:
                print(f"Not enough data for {symbol}, only {available_days} days of data available. Using available data.")

        
            
            return high_prices, low_prices, close_prices, open_prices
        else:
            print(f"Polygon.io'dan {symbol} için veri alınamadı. Hata: {response.status_code}")
            return None, None, None
    except requests.exceptions.RequestException as e:
        print(f"Veri alınırken hata oluştu: {e}")
        return None, None, None