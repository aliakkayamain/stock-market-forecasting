import numpy as np
from api.helpers.stockPrediction import predict_future_stock, load_model_for_symbol  
from api.helpers.weekend import get_previous_business_day, get_next_business_day
from api.helpers.buysell import enhanced_buy_sell 
from datetime import datetime, timedelta
from api.helpers.stockPrediction import load_symbols
from api.helpers.getHistoricalData import get_historical_data
from config.config import Config

symbols_file = Config.symbols_file
model_dir = Config.model_dir

def predict_stockAll(symbol, model_dir, lookback=5, future_days=1):
    """
    Belirtilen sembol için modeli kullanarak gelecekteki fiyatları tahmin eder.
    Geçmiş 7 gün kapanış fiyatlarını ve bir sonraki günün tahminini döner.
    """

    end_date = get_previous_business_day(datetime.today()).strftime("%Y-%m-%d")
    start_date = get_previous_business_day(datetime.today() - timedelta(days=8)).strftime("%Y-%m-%d")

    predictions = predict_future_stock(symbol, model_dir, start_date, end_date, lookback, future_days)

    high_prices, low_prices, close_prices, open_prices= get_historical_data(symbol, start_date, end_date)
    
    if predictions:
        last_closing_value = predictions[-1]  
        buy_sell = enhanced_buy_sell(last_closing_value, symbol)  

        prediction_date = get_next_business_day(datetime.today()).strftime("%Y-%m-%d")
        
        real_values = {
            "open": open_prices[-5:],     # Son 5 günün açılış fiyatları
            "high": high_prices[-5:],     # Son 5 günün en yüksek fiyatları
            "low": low_prices[-5:],       # Son 5 günün en düşük fiyatları
            "close": close_prices[-5:]    # Son 5 günün kapanış fiyatları
        }

        return {
            "symbol": symbol,
            "predict": round(predictions[0], 2),  
            "buysell": buy_sell,
            "real_value": real_values,
            "forecast_date": prediction_date
        }
    else:
        return {'error': f"Could not generate predictions for {symbol}"}


symbols = load_symbols(symbols_file)
print(f"yüklenen semboller-------------------------------------------------------------------: {symbols}") 


def predict_for_all(symbols, model_dir):
    """
    Tüm semboller için tahmin yapar ve sonuçları JSON formatında döner.
    """
    predictions = []

    for symbol in symbols:
        prediction = predict_stockAll(symbol, model_dir)
        if "error" not in prediction:
            predictions.append(prediction)

    return {"stocks": predictions}







