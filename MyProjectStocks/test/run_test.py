from fetch_data import fetch_stock_data
from predict import predict_last_week
from plot_results import plot_results
from evaluate import evaluate_predictions

SYMBOLS = [
   "AAPL", "AMZN", "JPM", "MSFT", "WMT" ]

"""['A', 'AAL', 'AAPL', 'ABBV', 'ABNB', 'ABT', 'ACGL', 'ACN', 'ADBE', 'ADI', 
 'ADM', 'AEE', 'AEP', 'AES', 'AFL', 'AIG', 'AKAM', 'ALB', 'ALGN', 'ALL', 
 'ALLE', 'AMAT', 'AMCR', 'AMD', 'AME', 'AMGN', 'AMP', 'AMT', 'AMZN', 'ANET', 
 'ANSS', 'AON', 'AOS', 'APA', 'APD', 'APH', 'APTV', 'ARE', 'AWK', 'AXP', 
 'GOOG', 'GOOGL', 'LNT', 'MMM', 'MO']"""


API_KEY = "Jpdzf05nPJhqVB5qpNZx2VbmhwVF1spP"
MODEL_PATH = "/Users/tbai/Documents/MyProjectStocks/train/models/{symbol}_model.keras"
SCALER_PATH = "/Users/tbai/Documents/MyProjectStocks/train/scalers/{symbol}_scaler.pkl"


def main():
    for symbol in SYMBOLS:
        try:
            print(f"{symbol} için son 99 günlük veri çekiliyor...")
            df_full = fetch_stock_data(symbol, API_KEY)

            print(f"{symbol} için model ile son 5 gün tahmin ediliyor...")
            predicted_values, df_real = predict_last_week(MODEL_PATH.format(symbol=symbol), SCALER_PATH.format(symbol=symbol), df_full, symbol)

            rmse = evaluate_predictions(df_real['close'].values, predicted_values)
            print(f"{symbol} için RMSE: {rmse}")
            
            print("Gerçek Değerler:")
            print(df_real['close'].values)

            print("Tahmin Edilen Değerler:")
            print(predicted_values)
            
            

            plot_results(df_real['close'].values, predicted_values, df_real, df_full, symbol)
        
        except FileNotFoundError:
            print(f"Model veya scaler {symbol} için bulunamadı, bu hisseyi atlıyorum.")
        except Exception as e:
            print(f"{symbol} için hata oluştu: {e}")


if __name__ == "__main__":
    main()