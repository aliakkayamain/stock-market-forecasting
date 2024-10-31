import numpy as np 
from datetime import datetime, timedelta 
import requests
from config.config import Config


POLYGON_API_KEY = Config.POLYGON_API_KEY
def historical_data(symbol, days=99):
    """
    Belirtilen hisse senedi için Polygon.io'dan son 'days' kadar günün yüksek, düşük ve kapanış fiyatlarını alır.
    Eksik günler varsa sadece mevcut olan günlerle devam eder.
    """
    end_date = datetime.today().strftime("%Y-%m-%d")
    start_date = (datetime.today() - timedelta(days=days)).strftime("%Y-%m-%d")
    
    url = f"https://api.polygon.io/v2/aggs/ticker/{symbol}/range/1/day/{start_date}/{end_date}?adjusted=true&sort=asc&limit=120&apiKey={POLYGON_API_KEY}"
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200 and 'results' in data:
        close_prices = [day['c'] for day in data['results'] if 'c' in day]  
        high_prices = [day['h'] for day in data['results'] if 'h' in day]   
        low_prices = [day['l'] for day in data['results'] if 'l' in day]   
        
        available_days = len(close_prices)
        if available_days < days:
            print(f"Not enough data for {symbol}, only {available_days} days of data available. Using available data.")

        return high_prices, low_prices, close_prices
    else:
        print(f"Polygon.io'dan {symbol} için veri alınamadı. Hata: {response.status_code}")
        return None, None, None


# ADX Hesaplama Fonksiyonu
def calculate_adx(high, low, close, window=14):
    """
    ADX (Average Directional Index) hesaplar. 
    Yüksek (high), düşük (low) ve kapanış (close) verileri gerektirir.
    """
    
    if len(high) < window or len(low) < window or len(close) < window:
        print(f"Yeterli veri yok, {window} günlük ADX hesaplanamıyor.")
        return np.nan
    
    high = np.array(high)
    low = np.array(low)
    close = np.array(close)

    tr = np.maximum(high[1:], close[:-1]) - np.minimum(low[1:], close[:-1])
    plus_dm = np.where(high[1:] > high[:-1], high[1:] - high[:-1], 0)
    minus_dm = np.where(low[1:] < low[:-1], low[:-1] - low[1:], 0)
    
    plus_di = 100 * (plus_dm / tr)
    minus_di = 100 * (minus_dm / tr)
    dx = np.where(np.abs(plus_di + minus_di) == 0, 0, (np.abs(plus_di - minus_di) / np.where(np.abs(plus_di + minus_di) == 0, 1, np.abs(plus_di + minus_di))) * 100)
    adx = np.convolve(dx, np.ones(window) / window, mode='valid')
    
    return adx[-1]

# Stochastic Hesaplama Fonksiyonu
def calculate_stoch(high, low, close, window=14):
    if len(high) < window or len(low) < window or len(close) < window:
        print(f"Yeterli veri yok, {window} günlük Stochastic hesaplanamıyor.")
        return np.nan
    
    highest_high = np.max(high[-window:])
    lowest_low = np.min(low[-window:])
    stoch = 100 * ((close[-1] - lowest_low) / (highest_high - lowest_low))
    return stoch

# Stochastic RSI Hesaplama Fonksiyonu
def calculate_stochrsi(data, window=14):
    """
    StochRSI (Stochastic RSI) hesaplar.
    Verilen veri için RSI hesaplar ve daha sonra StochRSI formülünü uygular.
    """
    # Önce RSI değerlerini bir liste olarak hesaplayalım
    rsi_values = calculate_rsi(data, window)
    
    print(f"RSI Değerleri Uzunluğu: {len(rsi_values)}, Gereken Min Veri: {window * 2}")
    print(f"RSI Değerleri: {rsi_values}")

    if len(rsi_values) < window:
        print(f"Yeterli veri yok, {window} günlük StochRSI hesaplanamıyor.")
        return np.nan

    # StochRSI hesaplaması
    rsi_min = np.min(rsi_values[-window:]) 
    rsi_max = np.max(rsi_values[-window:])  
    
    # StochRSI formülü
    if rsi_max != rsi_min:
        stochrsi = (rsi_values[-1] - rsi_min) / (rsi_max - rsi_min)
    else:
        stochrsi = 0  

    return stochrsi


# Williams %R Hesaplama Fonksiyonu
def calculate_williams_r(high, low, close, window=14):
    if len(high) < window or len(low) < window or len(close) < window:
        print(f"Yeterli veri yok, {window} günlük Williams %R hesaplanamıyor.")
        return np.nan
    
    highest_high = np.max(high[-window:])
    lowest_low = np.min(low[-window:])
    williams_r = -100 * ((highest_high - close[-1]) / (highest_high - lowest_low))
    return williams_r

# ATR Hesaplama Fonksiyonu
def calculate_atr(high, low, close, window=14):
    if len(high) < window or len(low) < window or len(close) < window:
        print(f"Yeterli veri yok, {window} günlük ATR hesaplanamıyor.")
        return np.nan
    
    tr = np.maximum(high[1:], close[:-1]) - np.minimum(low[1:], close[:-1])
    atr = np.convolve(tr, np.ones(window) / window, mode='valid')
    return atr[-1]

# CCI Hesaplama Fonksiyonu
def calculate_cci(high, low, close, window=14):
    """
    CCI (Commodity Channel Index) hesaplar.
    """
    
    if len(high) < window or len(low) < window or len(close) < window:
        print(f"Yeterli veri yok, {window} günlük CCI hesaplanamıyor.")
        return np.nan
    
    high = np.array(high)
    low = np.array(low)
    close = np.array(close)
    
 
    tp = (high + low + close) / 3
    ma = np.mean(tp[-window:])  
    mad = np.mean(np.abs(tp[-window:] - ma))  
    cci = (tp[-1] - ma) / (0.015 * mad)  
    
    return cci

# ROC Hesaplama Fonksiyonu
def calculate_roc(close, window=14):
    if len(close) < window:
        print(f"Yeterli veri yok, {window} günlük ROC hesaplanamıyor.")
        return np.nan
    
    roc = 100 * ((close[-1] - close[-window]) / close[-window])
    return roc

# Bull/Bear Power Hesaplama Fonksiyonu
def calculate_bull_bear_power(high, low, close, window=13):
    if len(high) < window or len(low) < window or len(close) < window:
        print(f"Yeterli veri yok, {window} günlük Bull/Bear Power hesaplanamıyor.")
        return np.nan, np.nan
    
    bull_power = high[-1] - np.mean(close[-window:])
    bear_power = low[-1] - np.mean(close[-window:])
    return bull_power, bear_power

# Hareketli Ortalama Hesaplama Fonksiyonu
def calculate_moving_average(data, window_size):
    """
    Basit hareketli ortalamayı hesaplar. Yalnızca son `window_size` kadar veriyi kullanır.
    """
    if len(data) < window_size:
        print(f"Yeterli veri yok, {window_size} günlük hareketli ortalama hesaplanamıyor.")
        return [np.nan]
    
    data = data[-window_size:]
    return np.convolve(data, np.ones(window_size) / window_size, mode='valid')

def calculate_rsi(data, window=14):
    """
    RSI (Relative Strength Index) hesaplar ve bir liste döndürür.
    """
    if len(data) < window:
        print(f"Yeterli veri yok, {window} günlük RSI hesaplanamıyor.")
        return np.array([]) 

    delta = np.diff(data)
    gain = np.where(delta > 0, delta, 0)
    loss = np.where(delta < 0, -delta, 0)

    avg_gain = np.mean(gain[:window])
    avg_loss = np.mean(loss[:window])

    if avg_loss == 0:
        rs = 0
    else:
        rs = avg_gain / avg_loss

    rsi = 100 - (100 / (1 + rs))
    rsi_values = [rsi]

    for i in range(window, len(data)):
        gain_value = gain[i - 1]
        loss_value = loss[i - 1]

        avg_gain = ((avg_gain * (window - 1)) + gain_value) / window
        avg_loss = ((avg_loss * (window - 1)) + loss_value) / window

        if avg_loss == 0:
            rs = 0
        else:
            rs = avg_gain / avg_loss

        rsi = 100 - (100 / (1 + rs))
        rsi_values.append(rsi)

    return np.array(rsi_values)

def calculate_macd(data, short_window=12, long_window=26, signal_window=9):
    """
    MACD (Moving Average Convergence Divergence) hesaplar.
    """
    if len(data) < long_window:
        print(f"Yeterli veri yok, MACD hesaplanamıyor. En az {long_window} gün verisi gerekiyor.")
        return np.nan, np.nan


    short_ma = np.convolve(data, np.ones(short_window) / short_window, mode='valid')
    long_ma = np.convolve(data, np.ones(long_window) / long_window, mode='valid')


    short_ma = short_ma[-len(long_ma):]

 
    macd = short_ma - long_ma
    signal = np.convolve(macd, np.ones(signal_window) / signal_window, mode='valid')

    return macd[-1], signal[-1]



def enhanced_buy_sell(predicted_price, symbol, days=99):
    """
    Gelişmiş 'al-sat' stratejisi.
    İndikatörler: Hareketli Ortalamalar, RSI, MACD, Stoch, Williams %R, ADX, ATR, CCI, ROC, Bull/Bear Power.
    """
    
    # Tarihsel verileri alalım
    high, low, close = historical_data(symbol, days)
    
    if high is None or low is None or close is None:
        return "Veri alınamadı"

    if len(close) < 28: 
        print(f"Yeterli veri yok, 28 günlük veri sağlanamıyor. Mevcut gün sayısı: {len(close)}")
        return "bekle"
    
    # Diğer indikatör hesaplamaları
    short_ma_window = 20  
    long_ma_window = 50  

    if len(close) < long_ma_window:
        print("Yeterli veri yok, bekle moduna geçiliyor.")
        return "bekle"
    
    short_ma = calculate_moving_average(close, short_ma_window)
    long_ma = calculate_moving_average(close, long_ma_window)

    rsi = calculate_rsi(close, window=14)  
    macd, signal = calculate_macd(close, short_window=12, long_window=26, signal_window=9)

    stoch = calculate_stoch(high[-14:], low[-14:], close[-14:])
    stochrsi = calculate_stochrsi(close)  # window=14 varsayılan olarak kullanılıyor
    williams_r = calculate_williams_r(high[-14:], low[-14:], close[-14:])
    adx = calculate_adx(high[-14:], low[-14:], close[-14:])
    atr = calculate_atr(high[-14:], low[-14:], close[-14:])
    cci = calculate_cci(high[-14:], low[-14:], close[-14:])
    roc = calculate_roc(close[-14:])
    bull_power, bear_power = calculate_bull_bear_power(high[-13:], low[-13:], close[-13:])
    
    previous_price = close[-1]
    price_change_percentage = abs((predicted_price - previous_price) / previous_price) * 100

    # Gelişmiş al-sat stratejisi mantığı
    if adx > 25:  # ADX > 25 ise trend güçlü
        if np.any(rsi < 30) and np.any(macd > signal):
            return "buy strong"  #
        elif np.any(rsi > 70) and np.any(macd < signal):
            return "sell strong"  
        elif stoch < 20 or williams_r < -80:
            return "buy"  
        elif stoch > 80 or williams_r > -20:
            return "sell"  
        elif short_ma > long_ma and price_change_percentage > 1:
            return "buy strong"  
        elif short_ma < long_ma and price_change_percentage > 1:
            return "sell strong"  
        else:
            return "notr"  
    else:  # ADX < 25 ise trend zayıf
        if stoch < 20 and np.any(rsi < 30):
            return "buy"  
        elif stoch > 80 and np.any(rsi > 70):
            return "sell" 
        elif short_ma > long_ma and np.any(macd > signal):
            return "buy"  
        elif short_ma < long_ma and np.any(macd < signal):
            return "sell"  
        else:
            return "wait"  
        
    """
    eski al sat stratejimiz
    if adx > 2 and (np.any(rsi < 30) or np.any(macd > signal)):
        return "guclu al"
    elif adx > 2 and (np.any(rsi > 70) or np.any(macd < signal)):
        return "guclu sat"
    elif stoch < 20 and williams_r < -80:
        return "al"
    elif stoch > 80 and williams_r > -20:
        return "sat"
    elif abs(roc) < 1 and price_change_percentage < 1:
        return "notr"
    
    return "bekle"""






