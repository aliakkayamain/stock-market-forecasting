import pandas as pd
import os


"""
    iki csv dosyasının arasındaki farklarI çıkarıp farklı_hisseler olarak kayıt eden kod
"""


# İlk CSV dosyasını oku
csv1_path = "/Users/tbai/Documents/Vsanaliz/analiz/project/ABD/Data/sp500_symbols.csv"  # İlk CSV dosyanızın yolu (Symbol sütunu var)
csv2_path = "/Users/tbai/Documents/Vsanaliz/analiz/output/kayitli_hisseler.csv"  # İkinci CSV dosyanızın yolu (HisseSembolu sütunu var)


output_dir = "output"  
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

output_csv_path = os.path.join(output_dir, "farkli_hisseler.csv")  

df1 = pd.read_csv(csv1_path)
df2 = pd.read_csv(csv2_path)

print("df1 sütunları:", df1.columns)
print("df2 sütunları:", df2.columns)

df1_column = 'Symbol'
df2_column = 'HisseSembolu'

common = pd.merge(df1, df2, left_on=df1_column, right_on=df2_column)

df1_unique = df1[~df1[df1_column].isin(common[df1_column])]
df2_unique = df2[~df2[df2_column].isin(common[df2_column])]

df_diff = pd.concat([df1_unique[[df1_column]], df2_unique[[df2_column]]])

df_diff = pd.DataFrame(df_diff.stack().reset_index(drop=True), columns=['FarkliHisseler'])


df_diff.to_csv(output_csv_path, index=False)

print(f"Farklı olan hisse sembolleri {output_csv_path} dosyasına kaydedildi.")