from keras.models import Sequential
from keras.layers import LSTM, Dropout, Dense
from keras.callbacks import EarlyStopping
from sklearn.model_selection import KFold



def train_lstm_model(x_train, y_train, symbol, batch_size=2):
    model = Sequential()
    
    # İlk LSTM katmanı (100 units)
    model.add(LSTM(units=100, return_sequences=True, input_shape=(x_train.shape[1], x_train.shape[2])))
    model.add(Dropout(0.2))  # Dropout oranı
    
    # İkinci LSTM katmanı (80 units)
    model.add(LSTM(units=80, return_sequences=True))
    model.add(Dropout(0.3))  # Dropout oranı
    
    # Üçüncü LSTM katmanı (50 units)
    model.add(LSTM(units=50, return_sequences=False))
    model.add(Dropout(0.3))  # Dropout oranı
    
    # Çıkış katmanı
    model.add(Dense(1))  # Kapanış fiyatını tahmin eden 1 çıktı birimi

    # Modeli derle
    model.compile(loss='mean_squared_error', optimizer='adam', metrics=['mean_absolute_error'])
    
    model.summary()  # Modelin özetini görmek için
    
    # Early Stopping: validation loss 3 ardışık epoch boyunca iyileşmezse durdur
    early_stopping = EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True)
    
    # K-Fold Cross-Validation
    kf = KFold(n_splits=5)
    for train_index, test_index in kf.split(x_train):
        x_train_fold, x_val_fold = x_train[train_index], x_train[test_index]
        y_train_fold, y_val_fold = y_train[train_index], y_train[test_index]

        # Modeli her fold için eğit
        model.fit(x_train_fold, y_train_fold, 
                  validation_data=(x_val_fold, y_val_fold), 
                  epochs=50,  # Eğitim için epoch sayısı azaltıldı
                  batch_size=batch_size, 
                  callbacks=[early_stopping])

    # Modeli kaydet
    model.save(f"/Users/tbai/Documents/MyProjectStocks/train/models/{symbol}_model.keras")
    
    print(f"{symbol} için model başarıyla eğitildi ve kaydedildi.")

















"""
#ikinci LSTM modeli

def train_lstm_model(x_train, y_train, symbol, batch_size=8):
    model = Sequential()
    
    # İlk LSTM katmanı (50 units)
    model.add(LSTM(units=50, return_sequences=True, input_shape=(x_train.shape[1], x_train.shape[2])))
    model.add(Dropout(0.3))  # Daha düşük dropout oranı
    
    # İlk LSTM katmanı (50 units)
    model.add(LSTM(units=80, return_sequences=True, input_shape=(x_train.shape[1], x_train.shape[2])))
    model.add(Dropout(0.3))  # Daha düşük dropout oranı
    
    # İlk LSTM katmanı (50 units)
    model.add(LSTM(units=120, return_sequences=True, input_shape=(x_train.shape[1], x_train.shape[2])))
    model.add(Dropout(0.3))  # Daha düşük dropout oranı
    
    # İlk LSTM katmanı (50 units)
    model.add(LSTM(units=80, return_sequences=True, input_shape=(x_train.shape[1], x_train.shape[2])))
    model.add(Dropout(0.2))  # Daha düşük dropout oranı
    
    # İlk LSTM katmanı (50 units)
    model.add(LSTM(units=50, return_sequences=True, input_shape=(x_train.shape[1], x_train.shape[2])))
    model.add(Dropout(0.2))  # Daha düşük dropout oranı
    
    # İkinci LSTM katmanı
    model.add(LSTM(units=50))
    
    # Dense katmanı: 2 çıktı birimi (burada iki farklı değer tahmin edilebilir, örneğin açılış ve kapanış)
    model.add(Dense(1))  # 2 çıktı
    
    # Modeli derle
    model.compile(loss='mean_squared_error', optimizer='adam', metrics=['mean_absolute_error'])
    
    model.summary()  # Modelin özetini görmek için
    
    # Early Stopping: validation loss 3 ardışık epoch boyunca iyileşmezse durdur
    early_stopping = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)
    
    # K-Fold Cross-Validation
    kf = KFold(n_splits=5)
    for train_index, test_index in kf.split(x_train):
        x_train_fold, x_val_fold = x_train[train_index], x_train[test_index]
        y_train_fold, y_val_fold = y_train[train_index], y_train[test_index]

        # Modeli her fold için eğit
        model.fit(x_train_fold, y_train_fold, 
                  validation_data=(x_val_fold, y_val_fold), 
                  epochs=50, 
                  batch_size=batch_size, 
                  callbacks=[early_stopping])

    # Modeli kaydet
    model.save(f"/Users/tbai/Documents/MyProjectStocks/train/models/{symbol}_model.keras")
    
    print(f"{symbol} için model başarıyla eğitildi ve kaydedildi.")





















#ilk lstm modelimiz !! model1
def train_lstm_model(x_train, y_train, symbol, batch_size=2):
    model = Sequential()
    
    # İlk LSTM katmanı (50 units, 'relu' aktivasyon fonksiyonu)
    model.add(LSTM(units=50, activation='relu', return_sequences=True, input_shape=(x_train.shape[1], x_train.shape[2])))
    model.add(Dropout(0.2))
    
    # İkinci LSTM katmanı (60 units)
    model.add(LSTM(units=60, activation='relu', return_sequences=True))
    model.add(Dropout(0.3))
    
    # Üçüncü LSTM katmanı (80 units)
    model.add(LSTM(units=80, activation='relu', return_sequences=True))
    model.add(Dropout(0.4))
    
    # Dördüncü LSTM katmanı (120 units, final layer)
    model.add(LSTM(units=120, activation='relu'))
    model.add(Dropout(0.5))
    
    # Çıkış katmanı
    model.add(Dense(units=1))  # Kapanış fiyatını tahmin etmek için 1 birim

    # Modelin özetini görmek için
    model.summary()

    # Modelin derlenmesi
    optimizer = Adam(learning_rate=0.001)  # Varsayılan değeri 0.001
    model.compile(optimizer=optimizer, loss='mean_squared_error')
    
    # Early Stopping: validation loss 3 ardışık epoch boyunca iyileşmezse durdur
    early_stopping = EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True)
    
    # K-Fold Cross-Validation
    kf = KFold(n_splits=5)  #
    for train_index, test_index in kf.split(x_train): 
        x_train_fold, x_val_fold = x_train[train_index], x_train[test_index]  # Eğitim ve doğrulama setlerini oluştur
        y_train_fold, y_val_fold = y_train[train_index], y_train[test_index]  # Etiketleri de aynı şekilde böl

        # Modeli her fold için eğit
        model.fit(x_train_fold, y_train_fold, 
                  validation_data=(x_val_fold, y_val_fold), 
                  epochs=50, 
                  batch_size=batch_size,  # Burada batch_size'ı belirtiyoruz
                  callbacks=[early_stopping])

    # Modeli kaydet
    model.save(f"/Users/tbai/Documents/MyProjectStocks/train/models/{symbol}_model.h5")
    
    print(f"{symbol} için model başarıyla eğitildi ve kaydedildi.")
"""