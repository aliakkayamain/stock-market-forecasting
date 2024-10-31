import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'Server')))

from Server.api.stocks.predictSymbol import predict_stock
from Server.api.stocks.predictionAll import load_symbols, predict_for_all,symbols_file, model_dir
from Server.api.stocks.analysis_module import load_predictions_from_file, analyze_predictions
from Server.api.helpers.saveJson import save_json_to_file
from Server.api.helpers.scheduler import  run_scheduler

from datetime import datetime
import os
import glob
import json

from flask_cors import CORS
from flask import Flask, request, jsonify 

import threading
from Server.config.config import Config

app = Flask(__name__)
CORS(app) 


@app.route('/api/v1/')
def hello_world():
    return 'PROJECT'


# bu endpoint ile tüm S&P 500 endeksine ait hisselerin bir sonraki gününü tahminliyoruz
@app.route('/api/v1/stocks', methods=['GET'])
def get_hisseler():
 
    symbols = load_symbols(symbols_file)
    predictions = predict_for_all(symbols, model_dir)

    current_time = datetime.now().strftime("%Y%m%d_%H%M")
    filename = f"predictions_{current_time}.json"

    save_json_to_file(predictions, filename=filename)
    return jsonify(predictions)


#Bir sonraki günü tahminlenen hisselerin geleceğe yöenlik 5 gününü daha tahminliyoruz
@app.route('/api/v1/stocks/<symbol>', methods=['GET'])
def predict(symbol):   
    lookback = int(request.args.get('lookback', 8))
    future_days = int(request.args.get('future_days', 5))

    return predict_stock(symbol, lookback=lookback, future_days=future_days)

#tahminleme yaptığımız hisseleri belirtilen tarihteki tahmininin gerkçek ile ne kadar tutarlı olduğunu gösteren enpoint
@app.route('/api/v1/stocks/analysis/<tarih>', methods=['GET'])
def analyze_all(tarih):
    predictions = load_predictions_from_file(tarih) 
    
    if not predictions:
        return jsonify({"error": "Tahmin verisi bulunamadı."}), 404

    analysis_results = analyze_predictions(predictions, tarih)
    if not analysis_results:
        return jsonify({"error": "Gerçek değerler bulunamadı."}), 500
    
    return jsonify({
        "analysis": analysis_results
    }), 200




@app.route('/api/v1/stocks/analysis/<symbol>/<tarih>', methods=['GET'])
def analyze_single_stock(symbol, tarih):
    """
    Verilen sembol (hisse kodu) ve tarihteki tahmin ile gerçek değerleri analiz eden endpoint.
    """
    # Tahminleri dosyadan yükle
    predictions = load_predictions_from_file(tarih) 
    
    if not predictions:
        return jsonify({"error": "Tahmin verisi bulunamadı."}), 404

    # Verilen sembol için tahmin verisini filtrele
    stock_prediction = next((pred for pred in predictions if pred.get('symbol') == symbol), None)

    if not stock_prediction:
        return jsonify({"error": f"{symbol} için tahmin verisi bulunamadı."}), 404

    # Analiz fonksiyonunu sadece bu sembol için çalıştır
    analysis_results = analyze_predictions([stock_prediction], tarih)
    
    if not analysis_results:
        return jsonify({"error": "Gerçek değerler bulunamadı."}), 500
    
    return jsonify({
        "analysis": analysis_results
    }), 200




#Tahminlemsi yapılan hissleri folder dan getiren enpoint
@app.route('/api/v1/latest-prediction', methods=['GET'])
def get_latest_prediction():
    folder_path = Config.predictions_directory
    json_files = glob.glob(os.path.join(folder_path, "*.json"))
    
    if not json_files:
        return jsonify({"error": "Herhangi bir .json dosyası bulunamadı."}), 404
    
    latest_file = max(json_files, key=os.path.getctime)
    
    with open(latest_file, 'r') as file:
        data = json.load(file)
    
    # Query parametre olarak sembol listesini alıyoruz, virgülle ayrılmış olabilir
    hisse_kodlari = request.args.get('stockcode')
    
    if hisse_kodlari:
        # Sembolleri virgülle ayırarak bir listeye çeviriyoruz ve tüm semboller için veri arıyoruz
        hisse_kodlari_list = [hisse_kodu.strip().upper() for hisse_kodu in hisse_kodlari.split(',')]
        
        # HisseKodu anahtarına göre filtreleme yapıyoruz // TAG değişince bu kısımda düzenleme yaplamılsın
        filtered_data = [stock for stock in data['stocks'] if stock['symbol'] in hisse_kodlari_list]
        
        if not filtered_data:
            return jsonify({"error": f"{hisse_kodlari} kodlarına uygun veri bulunamadı."}), 404
        
        return jsonify({"stocks": filtered_data})
    
    # Eğer sembol parametresi yoksa tüm veriyi döndürüyoruz
    return jsonify(data)




if __name__ == "__main__":

    scheduler_thread = threading.Thread(target=run_scheduler)
    scheduler_thread.daemon = True  
    scheduler_thread.start()

    app.run(debug=True)


