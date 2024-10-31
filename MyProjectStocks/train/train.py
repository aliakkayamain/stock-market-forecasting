import os
import pandas as pd
from fetch_data import fetch_stock_data
from preprocess import preprocess_data
from model import train_lstm_model
from datetime import datetime
import gc

# Ana eğitim fonksiyonu
def main():
    
    start_date = datetime(2014, 6, 1).date()  
    end_date = datetime(2024, 6, 1).date()    

    print(f"Veriler {start_date} - {end_date} tarih aralığında çekilecek.")

    symbols_df = pd.read_csv('/Users/tbai/Documents/MyProjectStocks/train/data/merged_symbols_names.csv')  # Sembolleri CSV'den çek
    api_key = "Jpdzf05nPJhqVB5qpNZx2VbmhwVF1spP"
    scaler_dir = "/Users/tbai/Documents/MyProjectStocks/train/scalers" 
    model_dir = "/Users/tbai/Documents/MyProjectStocks/train/models"  # Model klasörü
    
    os.makedirs(scaler_dir, exist_ok=True)  # Scaler dizinini oluştur
    os.makedirs(model_dir, exist_ok=True)  # Model dizinini oluştur

    for symbol in symbols_df['Symbol']:
        try:
            # Model dosyasını kontrol et (eğer .keras dosyası mevcutsa hisseyi atla)
            model_path = os.path.join(model_dir, f"{symbol}_model.keras")

            # Eğer model zaten varsa, eğitimi atla
            if os.path.exists(model_path):
                print(f"{symbol} modeli zaten mevcut, atlanıyor.")
                continue  # Sonraki hisseye geç
            
            print(f"{symbol} için {start_date} - {end_date} tarih aralığında veri çekiliyor...")
            df = fetch_stock_data(symbol, api_key, start_date, end_date)

            print(f"{symbol} için veri işleniyor ve scaler kaydediliyor...")
            x_train, y_train, scaler = preprocess_data(df, symbol, scaler_dir)
            print(f"Eğitim veri boyutu (x_train): {x_train.shape}")
            print(f"Eğitim etiket boyutu (y_train): {y_train.shape}")

            print(f"{symbol} için model eğitiliyor...")
            train_lstm_model(x_train, y_train, symbol)

            # Model başarıyla eğitildikten sonra belleği temizle
            del df, x_train, y_train, scaler
            gc.collect()  # Bellek yönetimi için
            
        except Exception as e:
            print(f"{symbol} için işlem sırasında hata oluştu: {e}")

if __name__ == "__main__":
    main()