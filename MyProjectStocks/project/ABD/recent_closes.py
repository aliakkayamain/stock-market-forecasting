import requests
from datetime import datetime, timedelta
from flask import jsonify

API_KEY = "Jpdzf05nPJhqVB5qpNZx2VbmhwVF1spP"  

def get_recent_closes(symbol):
    """
    Belirtilen sembol için son 5 günün kapanış verilerini döndürür.
    """
    end_date = datetime.today()
    start_date = end_date - timedelta(days=10)  
    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')
    
    url = f'https://api.polygon.io/v2/aggs/ticker/{symbol}/range/1/day/{start_date}/{end_date}?adjusted=true&sort=asc&limit=50000&apiKey={API_KEY}'
    response = requests.get(url)
    
    try:
        data = response.json()
    except ValueError:
        return jsonify({'error': 'API yanıtı JSON formatında değil.'}), 500


    if response.status_code == 200 and 'results' in data:
        closes = [
            {
                "date": datetime.fromtimestamp(day['t'] / 1000).strftime('%Y-%m-%d'),
                "close": day['c']
            }
            for day in data['results'][-5:] 
        ]
        return jsonify({symbol: closes})
    else:
        return jsonify({'error': f"Could not retrieve data for symbol {symbol}. API yanıtı: {data}"}), 500