import requests
from base64 import urlsafe_b64encode

API_KEY = ""
API_URL = "https://www.virustotal.com/api/v3/urls"

# Пример: проверка URL
def check_url_safety(url_to_check):
    # Шаг 1: Закодировать URL в base64
    url_id = urlsafe_b64encode(url_to_check.encode()).decode().strip("=")

    # Шаг 2: Отправить GET-запрос с закодированным URL
    headers = {
        "x-apikey": API_KEY  # Убедитесь, что ключ передается корректно
    }
    response = requests.get(f"{API_URL}/{url_id}", headers=headers)

    # Шаг 3: Отладочная информация
    print("Request URL:", f"{API_URL}/{url_id}")
    print("Headers:", headers)
    print("Status Code:", response.status_code)
    print("Response Text:", response.text)

    # Шаг 4: Вернуть JSON-ответ или обработать ошибку
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": response.json().get("message", f"HTTP Error {response.status_code}")}

# Проверка работы функции
result = check_url_safety("google.com")
print(result)
