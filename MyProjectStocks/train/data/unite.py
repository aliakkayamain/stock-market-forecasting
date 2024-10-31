import pandas as pd

file_paths = [
    '/Users/tbai/Documents/MyProjectStocks/train/data/djia_symbols_names.csv',
    '/Users/tbai/Documents/MyProjectStocks/train/data/nasdaq_composite_symbols_names.csv',
    '/Users/tbai/Documents/MyProjectStocks/train/data/russell_symbols_names.csv',
    '/Users/tbai/Documents/MyProjectStocks/train/data/sp500_symbols_names.csv'
]

dfs = []
for file_path in file_paths:
    try:
        # Hatalı satırları atlamak için satırları tek tek oku
        df = pd.read_csv(file_path, delimiter=',', on_bad_lines='skip')
        dfs.append(df)
    except Exception as e:
        print(f"{file_path} dosyası yüklenirken hata oluştu: {e}")

# DataFrame'leri birleştir ve "Symbol" sütununa göre tekrar edenleri kaldır
if dfs:
    merged_df = pd.concat(dfs, ignore_index=True).drop_duplicates(subset='Symbol')

    # Birleştirilmiş CSV dosyasını kaydet
    merged_df.to_csv('/Users/tbai/Documents/MyProjectStocks/train/data/merged_symbols_names.csv', index=False)
    print("Dosyalar başarıyla birleştirildi ve 'merged_symbols_names.csv' olarak kaydedildi.")
else:
    print("Birleştirilecek geçerli veri bulunamadı.")