import requests
import schedule
import time
import threading

def send_get_request():
    """
    Belirtilen URL'ye GET isteği gönderir ve yanıtı kontrol eder.
    """
    url = 'http://127.0.0.1:5000/stocks'  # Bu URL'yi config dosyasına da taşıyabilirsin
    try:
        response = requests.get(url)
        
        if response.status_code == 200:
            print("GET isteği başarılı:", response.json())
        else:
            print(f"GET isteği başarısız: {response.status_code}")
    except Exception as e:
        print(f"GET isteği sırasında bir hata oluştu: {e}")

def run_scheduler():
    """
    Belirtilen saatte GET isteği göndermek için bir zamanlayıcı başlatır.
    """
    schedule_time='23:59'
    schedule.every().day.at(schedule_time).do(send_get_request)  # Planlanan zaman
    print(f"run_scheduler bloğunun çalışması planlanan saat: {schedule_time}")
    while True:
        schedule.run_pending()
        time.sleep(10)

def start_scheduler_thread():
    """
    Zamanlayıcı fonksiyonunu bir iş parçacığında başlatır.
    """
    scheduler_thread = threading.Thread(target=run_scheduler)
    scheduler_thread.daemon = True 
    scheduler_thread.start()