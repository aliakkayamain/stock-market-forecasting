import pandas as pd

# Dosya yolları
merged_symbols_path = "/Users/tbai/Documents/MyProjectStocks/train/data/merged_symbols_names.csv"
error_symbols_path = "/Users/tbai/Documents/MyProjectStocks/train/data/error.csv"

# CSV dosyalarını yükle
# Hatalı satırları atlamak için on_bad_lines='skip' kullanıyoruz
merged_df = pd.read_csv(merged_symbols_path, on_bad_lines='skip')
error_df = pd.read_csv(error_symbols_path)

# 'error.csv' dosyasındaki sembolleri al
error_symbols = error_df['Symbol'].tolist()

# 'merged_symbols_names.csv' dosyasındaki sembollerden 'error.csv' sembollerini çıkar
filtered_df = merged_df[~merged_df['Symbol'].isin(error_symbols)]

# Sonucu tekrar 'merged_symbols_names.csv' dosyasına kaydet
filtered_df.to_csv(merged_symbols_path, index=False)

print("İşlem tamamlandı. 'error.csv' dosyasındaki semboller, 'merged_symbols_names.csv' dosyasından çıkarıldı.")