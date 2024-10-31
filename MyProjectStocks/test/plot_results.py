import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def plot_results(real_values, predicted_values, df_real, df_full, symbol):
    # Grafik oluşturma
    plt.figure(figsize=(24, 6))
    
    # Tüm 99 günlük veriyi çiz
    plt.plot(df_full.index, df_full['close'], color='blue', label='Gerçek Veriler (Son 99 Gün)')

    # Tahmin edilen son 5 günü çiz
    plt.plot(df_real.index, predicted_values, color='red', label='Tahmin Edilen Veriler (Son 5 Gün)')

    # Son 5 günün gerçek verilerini koyu yeşil ile çiz
    plt.plot(df_real.index, df_real['close'], color='darkgreen', label='Son 5 Gün Gerçek Veriler', linewidth=2.5)

    # Başlık ve etiketler
    plt.title(f'{symbol} - Son 5 Gün Tahmin vs Gerçek')
    plt.xlabel('Tarih')
    plt.ylabel('Kapanış Fiyatı')

    # Tarih eksenini formatla
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))  # Yıl-Ay-Gün formatı
    plt.gca().xaxis.set_major_locator(mdates.WeekdayLocator())  # Haftalık aralıklarla tarih göster
    
    # X eksenindeki tarihlerin birbirine girmemesi için döndürme
    plt.gcf().autofmt_xdate()

    plt.legend()
    plt.show()