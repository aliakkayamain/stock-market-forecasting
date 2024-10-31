from sklearn.metrics import mean_squared_error
import numpy as np

def evaluate_predictions(real_values, predicted_values):
    # Sadece kapanış fiyatı için RMSE hesapla
    rmse = np.sqrt(mean_squared_error(real_values, predicted_values))
    return rmse