import os
from flask import jsonify
from api.helpers.getHistoricalData import get_historical_data
from datetime import datetime, timedelta
from api.helpers.weekend import is_weekend, get_previous_business_day, get_next_business_day
from api.helpers.stockPrediction import predict_future_stock  # Ortak modülü burada kullanıyoruz
import os
from datetime import datetime, timedelta
from config.config import Config

MODEL_DIR = Config.model_dir

def predict_stock(symbol, lookback=5, future_days=5):
    """
    Belirtilen sembol için model tahminleri üretir ve sonuçları JSON formatında döner.
    Ayrıca geçmiş 7 günlük gerçek kapanış fiyatlarını ekler ve fark/oranları günceller.
    """
    model_path = os.path.join(MODEL_DIR, f"{symbol}_model.h5")

    print(f"Tahmin öncesi predict_stock içindeki model yolu------------------------------------------------------------------------------: {model_path}")

    if not os.path.exists(model_path):
        return jsonify({'error': f"Model for symbol {symbol} not found"}), 404

    end_date = get_previous_business_day(datetime.today()).strftime("%Y-%m-%d")
    start_date = get_previous_business_day(datetime.today() - timedelta(days=8)).strftime("%Y-%m-%d")


    high_prices, low_prices, close_prices, open_prices= get_historical_data(symbol, start_date, end_date)

    if close_prices is None:
        return jsonify({'error': f"Could not fetch historical data for {symbol}"}), 500

    
    start_date_model = get_previous_business_day(datetime.today() - timedelta(days=lookback)).strftime("%Y-%m-%d")

   
    predictions = predict_future_stock(symbol, MODEL_DIR, start_date_model, end_date, lookback, future_days)

    if predictions:
        symbol_predictions = []

        current_date = get_previous_business_day(datetime.today())
        for i in range(len(close_prices)-1, -1, -1):
            if i == 0:
                fark = None
                oran = None
            else:
                fark = close_prices[i] - close_prices[i-1]
                oran = (fark / close_prices[i-1]) * 100 if close_prices[i-1] != 0 else 0

            while is_weekend(current_date):
                current_date = get_previous_business_day(current_date - timedelta(days=1))

            symbol_predictions.insert(0, {  
                "close_value": float(close_prices[i]),
                "high_value": float(high_prices[i]),
                "low_value": float(low_prices[i]),
                "open_value": float(open_prices[i]),
                "difference": float(fark) if fark is not None else None,
                "ratio": float(oran) if oran is not None else None,
                "date": current_date.strftime("%Y-%m-%d")
            })

            current_date = get_previous_business_day(current_date - timedelta(days=1))

        last_closing_value = close_prices[-1]

        current_date = get_next_business_day(datetime.today())  
        for i, predicted_value in enumerate(predictions):
            while is_weekend(current_date):
                current_date = get_next_business_day(current_date)

            if i == 0:
                fark = predicted_value - last_closing_value
                oran = (fark / last_closing_value) * 100 if last_closing_value != 0 else 0
            else:
                fark = predicted_value - predictions[i-1]
                oran = (fark / predictions[i-1]) * 100 if predictions[i-1] != 0 else 0

            symbol_predictions.append({
                "predict": round(float(predicted_value),2), 
                "difference": float(fark),
                "raito": float(oran),
                "date": current_date.strftime("%Y-%m-%d")
            })

            current_date = get_next_business_day(current_date)  

        return jsonify({symbol: symbol_predictions}), 200  
    else:
        return jsonify({'error': f"Could not generate predictions for {symbol}"}), 500