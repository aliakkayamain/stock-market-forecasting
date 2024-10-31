import os
import json
from datetime import datetime, timedelta
from config.config import Config

def save_json_to_file(data, filename="predictions.json"):
    """
    ilgili klasöre json olarak kayıt eder
    """
    directory = Config.predictions_directory
    if not os.path.exists(directory):
        os.makedirs(directory)  
    
    # Dosyayı kaydetme
    file_path = os.path.join(directory, filename)
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)

    # Kaydetmeden sonra eski dosyaları temizleme
    clean_old_json_files(directory)

def clean_old_json_files(directory, days_threshold=30):
    """
    Bu fonksiyon, belirtilen dizindeki JSON dosyalarını tarar ve
    adı 30 günden daha eski olanları siler.
    """
    current_time = datetime.now()

    # Dizindeki tüm JSON dosyalarını bul
    for file_name in os.listdir(directory):
        if file_name.endswith(".json") and "predictions_" in file_name:
            print('## tararma yapılıyor 30 günden daha eski olan json silinecek....')
            # Dosya adından tarihi ayır
            try:
                # predictions_20240913_154803.json -> 20240913 kısmını alıyoruz
                date_str = file_name.split("_")[1]
                file_date = datetime.strptime(date_str, "%Y%m%d")
                
                # Tarihi karşılaştır, 30 günden eskiyse sil
                if (current_time - file_date).days > days_threshold:
                    file_path = os.path.join(directory, file_name)
                    os.remove(file_path)
                    print(f"Silinen eski dosya: {file_path}")
            except (IndexError, ValueError) as e:
                print(f"Dosya adı {file_name} geçerli bir tarih içermiyor: {e}")