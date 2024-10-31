import os
from dotenv import load_dotenv

# .env dosyası
load_dotenv()

class Config:
    # API anahtarlarını .env dosyasından çekiyoruz
    POLYGON_API_KEY = os.getenv("POLYGON_API_KEY")
    
    # Diğer dosya yolları
    symbols_file = "/Users/tbai/Documents/MyProjectStocks/project/ABD/Data/sp500_symbols.csv"
    model_dir = "/Users/tbai/Documents/MyProjectStocks/models/trained_models_ABD"
    predictions_directory = "/Users/tbai/Documents/MyProjectStocks/project/Server/All_past_predictions"