# MYPROJECTSTOCKS
# Hisse Senedi Tahminleme API'si

Bu proje, önceden eğitilmiş modelleri kullanarak hisse senedi tahmini hizmetleri sunan Flask tabanlı bir API'dir. Uygulama, S&P 500 şirketleri için hisse fiyatlarını tahmin eder ve ek olarak tarihsel analiz, al-sat stratejileri ve zamanlanmış tahmin işlemleri gibi özellikler içerir.

## Özellikler

- **Tüm Hisseler İçin Bir Sonraki Günü Tahmin Etme**: S&P 500'e dahil olan tüm hisseler için bir sonraki günü tahmin eder.
- **Gelecekteki Hisse Tahmini**: Belirli bir hisse için birkaç gün sonrasını tahmin eder.
- **Tarihsel Veri Analizi**: Belirli bir hissenin tahmin edilen ve gerçek performansını analiz eder.
- **Zamanlanmış GET İsteği**: Belirlenen bir saatte otomatik olarak hisse tahminlerini almak için planlama yapılır.

## Proje Yapısı

MYPROJECTSTOCKS/
	│
	├── .venv/                        # Proje için oluşturulmuş sanal ortam klasörü
	├── logs/                         # Log dosyalarının tutulduğu klasör
	├── models/                       # Yapay zeka modelleri ve eğitimli ağırlıkların tutulduğu klasör
	│   ├── trained_models_ABD/       # ABD hisse senetleri için eğitilmiş ağırlıklar
	│   ├── trained_models_ABD_GRU/   # ABD hisslerinin GRU modelleri için eğitilmiş ağırlıklar
	├── notebooks/                    # Jupyter Notebook dosyaları, analiz ve model geliştirme amaçlı
	├── output/                       # Çıktı dosyalarının tutulduğu klasör
	│   ├── csv/                      # CSV formatındaki çıktı dosyaları
	│   ├── image/                    # Görsel çıktılar
	│   └── scripts/                  # Yardımcı Python script dosyaları
	├── project/                      # Ana proje klasörü
	│   ├── ABD/                      # ABD hisse senetleri ile ilgili veri ve tahmin dosyaları
	│   │   ├── Data                  # Veri işleme de kullanılan verilerin olduğu yol
	│   │   ├── PolygonDataExtraction  # Polygon API ile veri çekimi işlemleri
	│   │   ├── futurePrediction.py   # Gelecekteki tahminleri gerçekleştiren modül
	│   │   ├── GRU_SP500_Predict.py  # SP500 GRU model tahminleri
	│   │   ├── GRU_SP500.py          # GRU modeli ile tahmin yapan modül
	│   │   ├── LSTM_SP500.ipynb      # LSTM modeli ile SP500 tahmini yapılan notebook dosyası
	│   │   ├── Prediction.py         # Genel tahmin modülü
	│   │   └── recent_closes.py      # En son kapanış verilerini alan modül
	│   ├── Server/                   # Sunucu tarafı kodlarının yer aldığı klasör
	│   │   ├── All_past_predictions/ # Geçmiş tahminlerin JSON formatında saklandığı klasör
	│   │   ├── api/                  # API fonksiyonlarını barındıran modüller
	│   │   │   ├── helpers/          # Yardımcı API fonksiyonları
	│   │   │   │   ├── buySell.py            # Al-Sat stratejileri
	│   │   │   │   ├── getHistoricalData.py  # Geçmiş veri çekme modülü
	│   │   │   │   ├── saveJson.py           # JSON formatında tahmin verilerini kaydetme
	│   │   │   │   ├── scheduler.py          # Zamanlayıcı ile işlem çalıştırma
	│   │   │   │   ├── stockPrediction.py    # Model kullanarak gelecekteki tahminleri gerçekleştiren modül
	│   │   │   │   └── weekend.py            # Hafta sonu ve iş günlerini işleyen yardımcı fonksiyonlar
	│	│   │   ├── stocks/            # Hisse senedi ile ilgili analiz ve tahmin modülleri
	│	│   │   │   ├── analysis_module.py  # Hisse tahminlerini analiz eden fonksiyonlar
	│	│   │   │   ├── predictionAll.py    # Tüm hisse senetleri için toplu tahmin işlemi
	│	│   │   │   └── predictSymbol.py    # Tek bir hisse senedi için tahmin işlemi
	│	│   ├── config/                   # Yapılandırma dosyalarının olduğu klasör
	│	│  		└── config.py             # Ortam değişkenleri ve yollar için yapılandırma
	├── .env                          # Ortam değişkenleri (örneğin, API anahtarları)
	├── .gitignore                    # Git izlememesi gereken dosya ve klasörler
	├── app.py                        # Ana Flask uygulaması ve API tanımlamaları
	├── README.md                     # Bu dökümantasyon dosyası
	└── requirements.txt              # Proje bağımlılıklarını içeren dosya




## Kurulum

1. Depoyu klonlayın:
   ```bash
   git clone https://github.com/kullanici-adi/proje-adi.git ///// oluşturulcak!!!!

2. proje dizinine gidin 
cd project

3.	Sanal ortam oluşturun:
python3 -m venv .venv
source .venv/bin/activate  # Linux/Mac için

4.	Gerekli paketleri yükleyin:
pip install -r requirements.txt

5.	Ortam değişkenlerini ayarlayın:
	•	Polygon.io API’sinden hisse senedi verilerini çekmek için POLYGON_API_KEY gerekli. Bunu ortam değişkeni olarak tanımladığınızdan emin olun veya config.py dosyasında varsayılan anahtarı kullanın.


## Kullanım

API’yi Çalıştırma

	1.	Sanal ortamı aktifleştirin:
    source .venv/bin/activate

    2.	Flask uygulamasını başlatın:
    python3 app.py


	3.	API’ye http://127.0.0.1:5000 adresinden erişebilirsiniz.



## Endpoint’ler

1. Ana Sayfa

	•	Endpoint: /
	•	Metot: GET
	•	Açıklama: Basit bir mesaj döner.

2. Tüm Hisseler İçin Tahmin Al

	•	Endpoint: /stocks
	•	Metot: GET
	•	Açıklama: S&P 500’e dahil tüm hisseler için bir sonraki gün tahmini yapar.

3. Belirli Bir Hisseyi Tahmin Et

	•	Endpoint: /stocks/<symbol>
	•	Metot: GET
	•	Açıklama: Belirli bir hisse için 5 gün sonrasını tahmin eder.
	•	Sorgu Parametreleri:
	•	lookback: Model için geçmişe yönelik kaç gün bakılacağı (varsayılan: 8).
	•	future_days: Kaç gün sonrasının tahmin edileceği (varsayılan: 5).

4. Tarihsel Analiz

	•	Endpoint: /stocks/analysis/<tarih>
	•	Metot: GET
	•	Açıklama: Tahmin edilen hisse fiyatlarının belirli bir tarihte gerçek değerlerle ne kadar uyumlu olduğunu analiz eder.

5. Son Tahmini Getir

	•	Endpoint: /latest-prediction
	•	Metot: GET
	•	Açıklama: En son oluşturulan JSON dosyasındaki hisse tahminlerini getirir.

6. Zamanlanmış İstekler

	•	Açıklama: Her gün saat 23:59’da zamanlanmış bir GET isteğiyle hisse tahminlerini otomatik olarak getirir.

Zamanlama ile Tahminler

Uygulama, schedule kütüphanesini kullanarak zamanlanmış GET isteklerini otomatik olarak gönderir. Bu görev, Server/api/scheduler.py dosyasında ayarlanmıştır.

Zaman formatının HH:MM formatına uygun olduğundan emin olun (örneğin 23:59).

Yapılandırma

	•	config.py dosyası şu ayarları içerir:
	•	POLYGON_API_KEY: Polygon.io API’sine erişim için kullanılan API anahtarı.
	•	symbols_file: S&P 500 hisse sembollerini içeren CSV dosyasının yolu.
	•	model_dir: Eğitilmiş modellerin bulunduğu dizinin yolu.
	•	predictions_directory: JSON tahmin dosyalarının saklandığı klasörün yolu.


## Test

API’yi test etmek için Postman veya cURL gibi araçları kullanabilirsiniz. Aşağıda cURL komutlarına örnekler verilmiştir:

# Tüm hisse tahminlemesi yap
curl http://127.0.0.1:5000/stocks

# Belirli bir hisseyi tahmin et 5 günlük 
curl http://127.0.0.1:5000/stocks/AAPL
curl http://127.0.0.1:5000/stocks/AAPL?lookback=8&future_days=5

# Belirli bir hisseyi tahmin et
curl http://127.0.0.1:5000/stocks/AAPL

# Tahmin analizi yap
curl http://127.0.0.1:5000/api/v1/stocks/analysis/<tarih>'  // yıl-ay-gün

# belirli bir hisse senedine (symbol) ve belirli bir tarihte (tarih) yapılan tahminlerin analizi için kullanılmaktadır.
curl http://127.0.0.1:5000/api/v1/stocks/analysis/<symbol>/<tarih>

# Son tahmini getir
curl http://127.0.0.1:5000/latest-prediction

# favori için tahminlemesi yapılmış hisseleri çek
curl http://localhost:5000/latest-prediction?stockcode=MMM,ABBV


## Polygon API 

polygon.io dan gelen API 

# aktif ve işlem gören tüm hisse senetlerini sorgulamak için aşağıdaki endpoint kullanılır
curl https://api.polygon.io/v3/reference/tickers?market=stocks&active=true&limit=1000&apiKey=Jpdzf05nPJhqVB5qpNZx2VbmhwVF1spP

# hisse senedi ile ilişkili olan şirket hakkında genel bilgiler verir. Bu bilgiler, web sitesinde şirket profilleri oluşturmak veya tahmin modelinde şirket bilgilerini kullanmak için ideal olabilir.
curl https://api.polygon.io/v1/meta/symbols/AAPL/company?apiKey=Jpdzf05nPJhqVB5qpNZx2VbmhwVF1spP

# hisse senedine ait şirket bilgilerini almak için aşağıdaki endpoint kullanılır
curl https://api.polygon.io/v1/meta/symbols/AAPL/company?apiKey=Jpdzf05nPJhqVB5qpNZx2VbmhwVF1spP

# Hisse piyasasının açık mı kapalı mı olduğunu gösteren endpoint
crul https://api.polygon.io/v1/marketstatus/now?apiKey=Jpdzf05nPJhqVB5qpNZx2VbmhwVF1spP

# hisse senedi haberlerine ulaşmak için kullanılır
curl https://api.polygon.io/v2/reference/news?ticker=AAPL&limit=5&apiKey=Jpdzf05nPJhqVB5qpNZx2VbmhwVF1spP

# Bugünün en çok kazanan hisselerini görebilmek için 
curl https://api.polygon.io/v2/snapshot/locale/us/markets/stocks/gainers?apiKey=Jpdzf05nPJhqVB5qpNZx2VbmhwVF1spP

# Bugünü en çok kaybettiren hisselerini görebilmek için 
curl https://api.polygon.io/v2/snapshot/locale/us/markets/stocks/gainers?apiKey=Jpdzf05nPJhqVB5qpNZx2VbmhwVF1spP


